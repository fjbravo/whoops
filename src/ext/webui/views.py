import logging
from typing import List, Type, TypeVar

import requests
from flask import current_app, redirect, render_template, request
from sqlalchemy.exc import IntegrityError

from src.ext.database import db
from src.models import Model
from src.models.cycle import WhoopCycle
from src.models.recovery import WhoopRecovery
from src.models.sleep import WhoopSleep
from src.models.workout import WhoopWorkout

logger = logging.getLogger(__name__)


def index():
    """
    Retrieve data from database.
    """
    cycles = _query_all(WhoopCycle)
    sleeps = _query_all(WhoopSleep)
    recoveries = _query_all(WhoopRecovery)
    workouts = _query_all(WhoopWorkout)

    return render_template(
        "index.html",
        cycles=cycles,
        sleeps=sleeps,
        recoveries=recoveries,
        workouts=workouts,
    )


def authorize():
    """
    Initiates the OAuth2 authorization flow by redirecting to the authorization URL.
    """

    whoo_client = current_app.config["WhoopClient"]

    return redirect(whoo_client.authorization_url(), code=302)


def callback():
    """
    Handles the OAuth2 callback and exchanges the authorization code for tokens.
    """
    code = request.args.get("code")
    state = request.args.get("state")

    if state != current_app.config["OAuthState"]:
        return "Error: Invalid state parameter", 400

    try:
        current_app.config["WhoopClient"].set_tokens(code)
        return "Authorized", 200

    except requests.HTTPError as e:
        return f"Failed to set tokens - {e}", 500


def export():
    """
    Retrieve and export Whoop data.
    """
    whoop_client = current_app.config["WhoopClient"]
    succeeded_count = {}
    try:
        cycles = whoop_client.get_cycles()
        sleeps = whoop_client.get_sleeps()
        recoveries = whoop_client.get_recoveries()
        workouts = whoop_client.get_workouts()

        datasets = {
            "Cycles": cycles,
            "Sleeps": sleeps,
            "Recoveries": recoveries,
            "Workouts": workouts,
        }

        with current_app.app_context():
            for name, dataset in datasets.items():
                succeeded_count[name] = _add_all(dataset)

    except requests.HTTPError as e:
        return f"Error retrieving Whoop data: {e}", 500

    return render_template(
        "export.html",
        cycles=cycles,
        sleeps=sleeps,
        recoveries=recoveries,
        workouts=workouts,
        succeeded=succeeded_count,
    )


def _query_all(model: Type[Model]):
    try:
        return db.session.query(model).all()
    except Exception:
        db.session.rollback()
        raise


def _add_all(models: List[Model]) -> int:
    """Add a list of models to the database."""
    if not models:
        return 0

    succeeded = 0
    for model in models:
        try:
            db.session.add(model)
            db.session.flush()
            succeeded += 1
        except IntegrityError:
            db.session.rollback()
        except Exception:
            raise

    db.session.commit()
    return succeeded
