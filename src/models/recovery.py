from datetime import datetime
from typing import Dict, Tuple

from src.ext.database import db


class WhoopRecovery(db.Model):
    __tablename__ = "whoop_recovery"

    sleep_id = db.Column(db.String(36), primary_key=True)
    cycle_id = db.Column(db.BigInteger, nullable=False)
    user_id = db.Column(db.BigInteger, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False)
    score_state = db.Column(db.String(15), nullable=False)
    user_calibrating = db.Column(db.Boolean, nullable=False)

    # Score fields
    recovery_score = db.Column(db.Integer, nullable=False)
    resting_heart_rate = db.Column(db.Integer, nullable=False)
    hrv_rmssd_ms = db.Column(db.Float, nullable=False)
    spo2_perc = db.Column(db.Float, nullable=False)
    skin_temp_celsius = db.Column(db.Float, nullable=False)

    @classmethod
    def from_json(cls, data: dict) -> "WhoopRecovery":
        score = data["score"]

        return cls(
            sleep_id=data["sleep_id"],  # type: ignore
            cycle_id=data["cycle_id"],  # type: ignore
            user_id=data["user_id"],  # type: ignore
            timestamp=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")),  # type: ignore
            updated_at=datetime.fromisoformat(  # type: ignore
                data["updated_at"].replace("Z", "+00:00")
            ),
            score_state=data["score_state"],  # type: ignore
            user_calibrating=score["user_calibrating"],  # type: ignore
            recovery_score=score["recovery_score"],  # type: ignore
            resting_heart_rate=score["resting_heart_rate"],  # type: ignore
            hrv_rmssd_ms=score["hrv_rmssd_milli"],  # type: ignore
            spo2_perc=score["spo2_percentage"],  # type: ignore
            skin_temp_celsius=score["skin_temp_celsius"],  # type: ignore
        )

    def to_dict(self) -> Dict:
        return {
            "sleep_id": self.sleep_id,
            "cycle_id": self.cycle_id,
            "user_id": self.user_id,
            "timestamp": self.timestamp.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "score_state": self.score_state,
            "user_calibrating": self.user_calibrating,
            "recovery_score": self.recovery_score,
            "resting_heart_rate": self.resting_heart_rate,
            "hrv_rmssd_ms": self.hrv_rmssd_ms,
            "spo2_perc": self.spo2_perc,
            "skin_temp_celsius": self.skin_temp_celsius,
        }
