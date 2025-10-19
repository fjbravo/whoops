from datetime import datetime
from typing import Dict, Tuple

from src.ext.database import db


class WhoopCycle(db.Model):
    __tablename__ = "whoop_cycle"

    id = db.Column(db.BigInteger, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False)
    start = db.Column(db.DateTime(timezone=True), nullable=False)
    end = db.Column(db.DateTime(timezone=True), nullable=True)
    timezone_offset = db.Column(db.String(10), nullable=False)
    score_state = db.Column(db.String(15), nullable=False)

    # Score fields
    strain = db.Column(db.Float, nullable=False)
    kilojoule = db.Column(db.Float, nullable=False)
    avg_heart_rate = db.Column(db.Integer, nullable=False)
    max_heart_rate = db.Column(db.Integer, nullable=False)

    @classmethod
    def from_json(cls, data: dict) -> "WhoopCycle":
        score = data["score"]

        return cls(
            id=data["id"],  # type: ignore
            timestamp=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")),  # type: ignore
            updated_at=datetime.fromisoformat(  # type: ignore
                data["updated_at"].replace("Z", "+00:00")
            ),
            start=datetime.fromisoformat(data["start"].replace("Z", "+00:00")),  # type: ignore
            end=datetime.fromisoformat(data["end"].replace("Z", "+00:00"))  # type: ignore
            if data.get("end")
            else None,
            timezone_offset=data["timezone_offset"],  # type: ignore
            score_state=data["score_state"],  # type: ignore
            strain=score["strain"],  # type: ignore
            kilojoule=score["kilojoule"],  # type: ignore
            avg_heart_rate=score["average_heart_rate"],  # type: ignore
            max_heart_rate=score["max_heart_rate"],  # type: ignore
        )
