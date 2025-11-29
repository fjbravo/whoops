import requests
from flask import abort, current_app, jsonify
from flask_restful import Resource

from src.ext.restapi.utils import WhoopsDbResource


class CycleDataResource(Resource):
    def get(self):
        return WhoopsDbResource().from_req()


class SleepDataResource(Resource):
    def get(self):
        return WhoopsDbResource().from_req()


class RecoveryDataResource(Resource):
    def get(self):
        return WhoopsDbResource().from_req()


class WorkoutDataResource(Resource):
    def get(self):
        return WhoopsDbResource().from_req()


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
