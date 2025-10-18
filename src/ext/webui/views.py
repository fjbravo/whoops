import logging

import requests
from flask import current_app, flash, redirect, render_template, request, url_for

from src.ext.database import add_all, query_all
from src.models.cycle import WhoopCycle
from src.models.recovery import WhoopRecovery
from src.models.sleep import WhoopSleep
from src.models.workout import WhoopWorkout

logger = logging.getLogger(__name__)


def index():
    """
    Retrieve data from database.
    """
    cycles = query_all(WhoopCycle)
    sleeps = query_all(WhoopSleep)
    recoveries = query_all(WhoopRecovery)
    workouts = query_all(WhoopWorkout)

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
        flash("Invalid OAuth state", "danger")

    try:
        current_app.config["WhoopClient"].set_tokens(code)
        flash("Authorized", "success")

    except requests.HTTPError as e:
        flash(f"Failed to set tokens: {e}", "danger")
        return redirect(url_for("webui.index"))

    return redirect(url_for("webui.index"))


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

        models = {
            "Cycles": cycles,
            "Sleeps": sleeps,
            "Recoveries": recoveries,
            "Workouts": workouts,
        }

        with current_app.app_context():
            for name, models in models.items():
                succeeded_count[name] = add_all(models)

    except requests.HTTPError as e:
        flash(f"Error retrieving Whoop data: {e}", "danger")
        return redirect(url_for("webui.index"))

    return render_template(
        "export.html",
        cycles=cycles,
        sleeps=sleeps,
        recoveries=recoveries,
        workouts=workouts,
        succeeded=succeeded_count,
    )
