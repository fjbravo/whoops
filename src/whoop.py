import logging
import random
import string
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, List, Type

import requests
from flask import current_app

from src.models import Model
from src.models.cycle import WhoopCycle
from src.models.recovery import WhoopRecovery
from src.models.sleep import WhoopSleep
from src.models.workout import WhoopWorkout

API_ENDPOINT = "https://api.prod.whoop.com/"
API_VERSION = "developer/v2"


logger = logging.getLogger(__name__)


class WhoopClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.tokens: Dict = {}
        self.refreshed_at: datetime = datetime.now()

    def set_tokens(self, auth_code: str) -> None:
        """Exchange authorization code for tokens."""
        params = self._build_token_params(
            grant_type="authorization_code",
            code=auth_code,
            redirect_uri=current_app.config["REDIRECT_URI"],
        )
        self.tokens = self._post_token_request(params)
        self.refreshed_at = datetime.now()

    def needs_refresh(self) -> bool:
        """Check if the token needs to be refreshed."""
        if not self.tokens:
            return True

        if datetime.now() - self.refreshed_at >= timedelta(minutes=55):
            return True

        return False

    def refresh_token(self):
        """Refresh the existing token if needed."""

        params = self._build_token_params(
            grant_type="refresh_token",
            refresh_token=self.tokens.get("refresh_token"),
            scope="offline",
        )

        self.tokens = self._post_token_request(params)
        self.refreshed_at = datetime.now()

    def authorization_url(self):
        """Build the OAuth authorization URL."""
        state = "".join(random.choices(string.ascii_letters + string.digits, k=16))
        current_app.config["OAuthState"] = state

        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": current_app.config["REDIRECT_URI"],
            "scope": "offline read:workout read:recovery read:sleep read:cycles",
            "state": state,
        }
        query = urllib.parse.urlencode(params)
        return f"{API_ENDPOINT}oauth/oauth2/auth?{query}"

    def get_cycles(self) -> List[WhoopCycle]:
        return self._fetch_paginated("cycle", WhoopCycle)

    def get_sleeps(self) -> List[WhoopSleep]:
        return self._fetch_paginated("activity/sleep", WhoopSleep)

    def get_recoveries(self) -> List[WhoopRecovery]:
        return self._fetch_paginated("recovery", WhoopRecovery)

    def get_workouts(self) -> List[WhoopWorkout]:
        return self._fetch_paginated("activity/workout", WhoopWorkout)

    def _fetch_paginated(
        self,
        endpoint: str,
        model_cls: Type[Model],
    ) -> List[Model]:
        """Generic method to fetch paginated data from the Whoop API."""
        base_url = f"{API_ENDPOINT}{API_VERSION}/{endpoint}"
        url = base_url
        results: List[Model] = []

        while url:
            response = requests.get(url, headers=self._auth_header())
            response.raise_for_status()
            data = response.json()

            records = data.get("records", [])
            results.extend(model_cls.from_json(r) for r in records)

            next_token = data.get("next_token")
            url = f"{base_url}?nextToken={next_token}" if next_token else None

        return results

    def _post_token_request(self, data: Dict) -> Dict:
        """Internal helper to post to the token endpoint."""
        url = f"{API_ENDPOINT}oauth/oauth2/token"
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()

    def _build_token_params(self, **overrides) -> Dict:
        """Base token params with overrides."""
        base = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        base.update(overrides)
        return base

    def _auth_header(self) -> Dict:
        if self.tokens:
            return {"Authorization": f"Bearer {self.tokens['access_token']}"}
        return {}
