import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    return int(value) if value else default


def _get_float(name: str, default: float) -> float:
    value = os.getenv(name)
    return float(value) if value else default


@dataclass
class Config:
    srt_id: str
    srt_password: str
    dep_station: str
    arr_station: str
    date: str
    time_start: str = "000000"
    time_end: str = "235959"
    adult_count: int = 1
    child_count: int = 0
    senior_count: int = 0
    seat_type: str = "GENERAL_FIRST"
    check_interval_min: float = 8.0
    check_interval_max: float = 15.0
    max_run_seconds: Optional[float] = None
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None

    @classmethod
    def from_env(cls) -> "Config":
        required = {
            "SRT_ID": os.getenv("SRT_ID"),
            "SRT_PASSWORD": os.getenv("SRT_PASSWORD"),
            "DEP_STATION": os.getenv("DEP_STATION"),
            "ARR_STATION": os.getenv("ARR_STATION"),
            "TRAIN_DATE": os.getenv("TRAIN_DATE"),
        }
        missing = [key for key, value in required.items() if not value]
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

        return cls(
            srt_id=required["SRT_ID"],
            srt_password=required["SRT_PASSWORD"],
            dep_station=required["DEP_STATION"],
            arr_station=required["ARR_STATION"],
            date=required["TRAIN_DATE"],
            time_start=os.getenv("TIME_START", "000000"),
            time_end=os.getenv("TIME_END", "235959"),
            adult_count=_get_int("ADULT_COUNT", 1),
            child_count=_get_int("CHILD_COUNT", 0),
            senior_count=_get_int("SENIOR_COUNT", 0),
            seat_type=os.getenv("SEAT_TYPE", "GENERAL_FIRST").upper(),
            check_interval_min=_get_float("CHECK_INTERVAL_MIN", 8.0),
            check_interval_max=_get_float("CHECK_INTERVAL_MAX", 15.0),
            max_run_seconds=(
                float(os.getenv("MAX_RUN_SECONDS")) if os.getenv("MAX_RUN_SECONDS") else None
            ),
            telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN") or None,
            telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID") or None,
        )
