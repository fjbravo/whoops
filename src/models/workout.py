from datetime import datetime

from src.ext.database import db


class WhoopWorkout(db.Model):
    __tablename__ = "whoop_workout"

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)
    start = db.Column(db.DateTime(timezone=True), nullable=False)
    end = db.Column(db.DateTime(timezone=True), nullable=False)
    timezone_offset = db.Column(db.String(10), nullable=True)
    sport_name = db.Column(db.String(32), nullable=False)
    score_state = db.Column(db.String(15), nullable=True)

    # Score fields
    strain = db.Column(db.Float, nullable=False)
    avg_heart_rate = db.Column(db.Integer, nullable=False)
    max_heart_rate = db.Column(db.Integer, nullable=False)
    kilojoule = db.Column(db.Float, nullable=False)
    percent_recorded = db.Column(db.Float, nullable=False)
    distance_meter = db.Column(db.Float, nullable=True)
    altitude_gain_meter = db.Column(db.Float, nullable=True)
    altitude_change_meter = db.Column(db.Float, nullable=True)
    zone_zero_milli = db.Column(db.Integer, nullable=True)
    zone_one_milli = db.Column(db.Integer, nullable=True)
    zone_two_milli = db.Column(db.Integer, nullable=True)
    zone_three_milli = db.Column(db.Integer, nullable=True)
    zone_four_milli = db.Column(db.Integer, nullable=True)
    zone_five_milli = db.Column(db.Integer, nullable=True)

    @classmethod
    def from_json(cls, data: dict) -> "WhoopWorkout":
        score = data.get("score", {})
        zones = score.get("zone_durations", {})

        return cls(
            id=data["id"],  # type: ignore
            user_id=data.get("user_id"),  # type: ignore
            timestamp=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")),  # type: ignore
            updated_at=datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00"))  # type: ignore
            if data.get("updated_at")
            else None,  # type: ignore
            start=datetime.fromisoformat(data["start"].replace("Z", "+00:00")),  # type: ignore
            end=datetime.fromisoformat(data["end"].replace("Z", "+00:00")),  # type: ignore
            timezone_offset=data.get("timezone_offset"),  # type: ignore
            sport_name=data.get("sport_name"),  # type: ignore
            score_state=data.get("score_state"),  # type: ignore
            strain=score.get("strain"),  # type: ignore
            avg_heart_rate=score.get("average_heart_rate"),  # type: ignore
            max_heart_rate=score.get("max_heart_rate"),  # type: ignore
            kilojoule=score.get("kilojoule"),  # type: ignore
            percent_recorded=score.get("percent_recorded"),  # type: ignore
            distance_meter=score.get("distance_meter"),  # type: ignore
            altitude_gain_meter=score.get("altitude_gain_meter"),  # type: ignore
            altitude_change_meter=score.get("altitude_change_meter"),  # type: ignore
            zone_zero_milli=zones.get("zone_zero_milli"),  # type: ignore
            zone_one_milli=zones.get("zone_one_milli"),  # type: ignore
            zone_two_milli=zones.get("zone_two_milli"),  # type: ignore
            zone_three_milli=zones.get("zone_three_milli"),  # type: ignore
            zone_four_milli=zones.get("zone_four_milli"),  # type: ignore
            zone_five_milli=zones.get("zone_five_milli"),  # type: ignore
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "timestamp": self.timestamp.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "timezone_offset": self.timezone_offset,
            "sport_name": self.sport_name,
            "score_state": self.score_state,
            "strain": self.strain,
            "avg_heart_rate": self.avg_heart_rate,
            "max_heart_rate": self.max_heart_rate,
            "kilojoule": self.kilojoule,
            "percent_recorded": self.percent_recorded,
            "distance_meter": self.distance_meter,
            "altitude_gain_meter": self.altitude_gain_meter,
            "altitude_change_meter": self.altitude_change_meter,
            "zone_zero_milli": self.zone_zero_milli,
            "zone_one_milli": self.zone_one_milli,
            "zone_two_milli": self.zone_two_milli,
            "zone_three_milli": self.zone_three_milli,
            "zone_four_milli": self.zone_four_milli,
            "zone_five_milli": self.zone_five_milli,
        }
