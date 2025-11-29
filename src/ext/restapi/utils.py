import logging
from datetime import datetime, timedelta, timezone

from flask_restful import request

from src.ext.database import query_all, query_all_between
from src.models import from_path
from src.utils import parseRange

logger = logging.getLogger(__name__)


class WhoopsDbResource:
    def from_req(self):
        try:
            model = from_path(request.path)
        except ValueError as e:
            return {"message": str(e)}, 400

        args = request.args.to_dict()
        range = args.get("range")

        if not range:
            records = query_all(model)
            return {"records": [r.to_dict() for r in records]}, 200

        try:
            range = parseRange(range)
        except ValueError as e:
            return {"message": str(e)}, 400

        now = datetime.now(tz=timezone.utc)
        start = now - timedelta(days=range + 1)

        records = query_all_between(model, start, now)

        return {"records": [r.to_dict() for r in records]}, 200
