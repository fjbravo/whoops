from flask import Blueprint
from flask_restful import Api

from .resources import (
    CycleDataResource,
    RecoveryDataResource,
    SleepDataResource,
    WhoopDataResource,
    WorkoutDataResource,
)

bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)


def init_app(app):
    api.add_resource(WhoopDataResource, "/whoop/data")
    api.add_resource(CycleDataResource, "/whoop/cycle")
    api.add_resource(RecoveryDataResource, "/whoop/recovery")
    api.add_resource(SleepDataResource, "/whoop/activity/sleep")
    api.add_resource(WorkoutDataResource, "/whoop/activity/workout")
    app.register_blueprint(bp)
