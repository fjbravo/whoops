import logging
from datetime import datetime
from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)

db = SQLAlchemy()


def query_all(model):
    try:
        return db.session.query(model).order_by(model.timestamp.desc()).all()
    except Exception:
        db.session.rollback()
        raise


def query_all_between(model, start: datetime, end: datetime) -> List:
    try:
        return (
            db.session.query(model)
            .filter(model.timestamp.between(start, end))
            .order_by(model.timestamp.desc())
            .all()
        )
    except Exception:
        db.session.rollback()
        raise


def add_all(models) -> int:
    """Add a list of models to the database."""
    if not models:
        return 0

    succeeded = 0
    for model in models:
        try:
            db.session.add(model)
            db.session.commit()
            succeeded += 1
        except IntegrityError:
            db.session.rollback()
        except Exception:
            raise

    return succeeded


def init_app(app):
    """Initializes the database extension."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
