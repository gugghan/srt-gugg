import pytest

from srt_bot.config import Config

REQUIRED_ENV = {
    "SRT_ID": "test_id",
    "SRT_PASSWORD": "test_password",
    "DEP_STATION": "수서",
    "ARR_STATION": "부산",
    "TRAIN_DATE": "20260710",
}


def test_from_env_reads_required_fields(monkeypatch):
    for key, value in REQUIRED_ENV.items():
        monkeypatch.setenv(key, value)

    config = Config.from_env()

    assert config.srt_id == "test_id"
    assert config.dep_station == "수서"
    assert config.arr_station == "부산"
    assert config.date == "20260710"
    assert config.time_start == "000000"
    assert config.time_end == "235959"
    assert config.adult_count == 1
    assert config.seat_type == "GENERAL_FIRST"


def test_from_env_missing_required_field_raises(monkeypatch):
    for key, value in REQUIRED_ENV.items():
        monkeypatch.setenv(key, value)
    monkeypatch.delenv("SRT_ID", raising=False)

    with pytest.raises(ValueError):
        Config.from_env()


def test_from_env_reads_optional_overrides(monkeypatch):
    for key, value in REQUIRED_ENV.items():
        monkeypatch.setenv(key, value)
    monkeypatch.setenv("TIME_START", "060000")
    monkeypatch.setenv("TIME_END", "120000")
    monkeypatch.setenv("ADULT_COUNT", "2")
    monkeypatch.setenv("SEAT_TYPE", "special_only")
    monkeypatch.setenv("CHECK_INTERVAL_MIN", "5")
    monkeypatch.setenv("CHECK_INTERVAL_MAX", "9")

    config = Config.from_env()

    assert config.time_start == "060000"
    assert config.time_end == "120000"
    assert config.adult_count == 2
    assert config.seat_type == "SPECIAL_ONLY"
    assert config.check_interval_min == 5.0
    assert config.check_interval_max == 9.0
