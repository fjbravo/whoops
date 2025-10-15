from datetime import datetime

from src.ext.database import db


class WhoopSleep(db.Model):
    __tablename__ = "whoop_sleep"

    id = db.Column(db.String, primary_key=True)
    cycle_id = db.Column(db.BigInteger, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)
    start = db.Column(db.DateTime(timezone=True), nullable=False)
    end = db.Column(db.DateTime(timezone=True), nullable=False)
    timezone_offset = db.Column(db.String, nullable=True)
    nap = db.Column(db.Boolean, nullable=True)
    score_state = db.Column(db.String, nullable=True)

    # Score fields
    respiratory_rate = db.Column(db.Float, nullable=False)
    performance_perc = db.Column(db.Integer, nullable=False)
    consistency_perc = db.Column(db.Integer, nullable=False)
    efficiency_perc = db.Column(db.Integer, nullable=False)

    # Stage summary
    total_in_bed_ms = db.Column(db.BigInteger, nullable=False)
    total_awake_ms = db.Column(db.BigInteger, nullable=False)
    total_no_data_ms = db.Column(db.BigInteger, nullable=True)
    total_light_sleep_ms = db.Column(db.BigInteger, nullable=False)
    total_slow_wave_sleep_ms = db.Column(db.BigInteger, nullable=False)
    total_rem_sleep_ms = db.Column(db.BigInteger, nullable=False)
    sleep_cycle_count = db.Column(db.Integer, nullable=False)
    disturbance_count = db.Column(db.Integer, nullable=False)

    # Sleep needed
    sleep_needed_baseline_ms = db.Column(db.BigInteger, nullable=False)
    sleep_debt_ms = db.Column(db.BigInteger, nullable=False)
    add_sleep_from_strain_ms = db.Column(db.BigInteger, nullable=False)
    add_sleep_from_nap_ms = db.Column(db.BigInteger, nullable=True)

    @classmethod
    def from_json(cls, data: dict) -> "WhoopSleep":
        score = data.get("score", {})
        stage = score.get("stage_summary", {})
        sleep_needed = score.get("sleep_needed", {})

        return cls(
            id=data["id"],  # type: ignore
            cycle_id=data["cycle_id"],  # type: ignore
            timestamp=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")),  # type: ignore
            updated_at=datetime.fromisoformat(  # type: ignore
                data["updated_at"].replace("Z", "+00:00")
            ),
            start=datetime.fromisoformat(data["start"].replace("Z", "+00:00")),  # type: ignore
            end=datetime.fromisoformat(data["end"].replace("Z", "+00:00")),  # type: ignore
            timezone_offset=data.get("timezone_offset"),  # type: ignore
            nap=data.get("nap"),  # type: ignore
            score_state=data.get("score_state"),  # type: ignore
            respiratory_rate=score.get("respiratory_rate"),  # type: ignore
            performance_perc=score.get("sleep_performance_percentage"),  # type: ignore
            consistency_perc=score.get("sleep_consistency_percentage"),  # type: ignore
            efficiency_perc=score.get("sleep_efficiency_percentage"),  # type: ignore
            total_in_bed_ms=stage.get("total_in_bed_time_milli"),  # type: ignore
            total_awake_ms=stage.get("total_awake_time_milli"),  # type: ignore
            total_no_data_ms=stage.get("total_no_data_time_milli"),  # type: ignore
            total_light_sleep_ms=stage.get("total_light_sleep_time_milli"),  # type: ignore
            total_slow_wave_sleep_ms=stage.get("total_slow_wave_sleep_time_milli"),  # type: ignore
            total_rem_sleep_ms=stage.get("total_rem_sleep_time_milli"),  # type: ignore
            sleep_cycle_count=stage.get("sleep_cycle_count"),  # type: ignore
            disturbance_count=stage.get("disturbance_count"),  # type: ignore
            sleep_needed_baseline_ms=sleep_needed.get("baseline_milli"),  # type: ignore
            sleep_debt_ms=sleep_needed.get("need_from_sleep_debt_milli"),  # type: ignore
            add_sleep_from_strain_ms=sleep_needed.get(  # type: ignore
                "need_from_recent_strain_milli"
            ),
            add_sleep_from_nap_ms=sleep_needed.get("need_from_recent_nap_milli"),  # type: ignore
        )
