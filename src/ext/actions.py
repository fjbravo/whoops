import logging

import requests
from apscheduler.schedulers.background import BackgroundScheduler

from .database import add_all

logger = logging.getLogger(__name__)


def refresh_token(app):
    whoop_client = app.config["WhoopClient"]
    if whoop_client.needs_refresh():
        try:
            whoop_client.refresh_token()
            logger.info("Token refreshed successfully.")
        except requests.HTTPError:
            logger.error("Manual authorization required. Visit /authorize.")


def export_action(app):
    whoop_client = app.config["WhoopClient"]

    try:
        cycles = whoop_client.get_cycles()
        sleeps = whoop_client.get_sleeps()
        recoveries = whoop_client.get_recoveries()
        workouts = whoop_client.get_workouts()

        with app.app_context():
            add_all(cycles)
            add_all(sleeps)
            add_all(recoveries)
            add_all(workouts)

        logger.info("Data exported successfully.")
    except requests.HTTPError as e:
        logger.error(e)


def init_app(app):
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        refresh_token,
        "interval",
        minutes=5,
        args=[app],
    )

    scheduler.add_job(
        export_action,
        "interval",
        hours=24,
        args=[app],
    )

    scheduler.start()
