from flask import Blueprint

from .views import authorize, callback, export, index

bp = Blueprint("webui", __name__, template_folder="templates")

bp.add_url_rule("/", view_func=index)
bp.add_url_rule("/authorize", view_func=authorize)
bp.add_url_rule("/callback", view_func=callback)
bp.add_url_rule("/export", view_func=export)


def init_app(app):
    """Initializes the web UI extension."""
    app.register_blueprint(bp)
