import logging

import requests
from flask import abort, current_app, jsonify
from flask_restful import Resource

logger = logging.getLogger(__name__)


class WhoopDataResource(Resource):
    def get(self):
        whoop_client = current_app.config["WhoopClient"]

        try:
            cycles = [c.to_dict() for c in whoop_client.get_cycles()]
            sleeps = [s.to_dict() for s in whoop_client.get_sleeps()]
            recoveries = [r.to_dict() for r in whoop_client.get_recoveries()]
            workouts = [w.to_dict() for w in whoop_client.get_workouts()]

            data = {
                "cycles": cycles,
                "sleeps": sleeps,
                "recoveries": recoveries,
                "workouts": workouts,
            }
        except requests.HTTPError as e:
            abort(
                e.response.status_code,
                description=e,
            )

        return jsonify(data)
