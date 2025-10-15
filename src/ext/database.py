from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    """Initializes the database extension."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
