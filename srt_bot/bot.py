import logging
import random
import time
from typing import List, Optional

from SRT import SRT, SRTError, SRTLoginError, SRTNotLoggedInError, SRTResponseError
from SRT.passenger import Adult, Child, Senior
from SRT.seat_type import SeatType

from .config import Config
from .notifier import TelegramNotifier

logger = logging.getLogger(__name__)


class SRTBot:
    def __init__(self, config: Config):
        self.config = config
        self.notifier = TelegramNotifier(config.telegram_bot_token, config.telegram_chat_id)
        self.srt: Optional[SRT] = None

    def _passengers(self) -> List:
        passengers = []
        passengers += [Adult()] * self.config.adult_count
        passengers += [Child()] * self.config.child_count
        passengers += [Senior()] * self.config.senior_count
        return passengers or [Adult()]

    def _login(self) -> None:
        logger.info("Logging in to SRT as %s", self.config.srt_id)
        self.srt = SRT(self.config.srt_id, self.config.srt_password, auto_login=True)

    def _seat_available(self, train) -> bool:
        seat_type = self.config.seat_type
        if seat_type == "GENERAL_ONLY":
            return train.general_seat_available()
        if seat_type == "SPECIAL_ONLY":
            return train.special_seat_available()
        return train.seat_available()

    def _search(self):
        return self.srt.search_train(
            dep=self.config.dep_station,
            arr=self.config.arr_station,
            date=self.config.date,
            time=self.config.time_start,
            time_limit=self.config.time_end,
            available_only=False,
        )

    def _try_reserve(self, trains) -> bool:
        passengers = self._passengers()
        try:
            seat_type = SeatType[self.config.seat_type]
        except KeyError:
            logger.warning("Unknown SEAT_TYPE %r, falling back to GENERAL_FIRST", self.config.seat_type)
            seat_type = SeatType.GENERAL_FIRST

        for train in trains:
            if not self._seat_available(train):
                continue

            logger.info(
                "Seat available on train %s (%s -> %s), attempting reservation",
                train.train_number,
                train.dep_time,
                train.arr_time,
            )
            try:
                reservation = self.srt.reserve(
                    train, passengers=passengers, special_seat=seat_type
                )
            except SRTError as exc:
                logger.warning("Reservation attempt failed for train %s: %s", train.train_number, exc)
                continue

            message = (
                "SRT 예매 성공!\n"
                f"{self.config.dep_station} -> {self.config.arr_station}\n"
                f"열차 {train.train_number} ({train.dep_time} 출발)\n"
                f"예약번호: {getattr(reservation, 'reservation_number', 'N/A')}"
            )
            logger.info(message)
            self.notifier.send(message)
            return True

        return False

    def run(self) -> bool:
        """Search and attempt reservation until success or the time budget runs out.

        Returns True if a reservation was made, False if the (optional)
        max_run_seconds budget was exhausted first. With no budget configured
        this blocks forever until a reservation succeeds.
        """
        self._login()
        self.notifier.send(
            "SRT 자동예매 봇을 시작합니다: "
            f"{self.config.dep_station} -> {self.config.arr_station}, "
            f"{self.config.date} {self.config.time_start}~{self.config.time_end}"
        )

        start_time = time.monotonic()
        attempt = 0
        while True:
            if (
                self.config.max_run_seconds is not None
                and time.monotonic() - start_time >= self.config.max_run_seconds
            ):
                logger.info(
                    "Time budget of %.0fs exhausted without a reservation; "
                    "exiting for the next scheduled run",
                    self.config.max_run_seconds,
                )
                return False

            attempt += 1
            try:
                trains = self._search()
                if self._try_reserve(trains):
                    return True
                logger.info("Attempt #%d: no seats available yet", attempt)
            except SRTNotLoggedInError:
                logger.warning("Session expired, re-logging in")
                self._login()
            except SRTLoginError as exc:
                logger.error("Login failed: %s", exc)
                raise
            except SRTResponseError as exc:
                logger.warning("Temporary SRT response error: %s", exc)
            except SRTError as exc:
                logger.warning("SRT error: %s", exc)
            except Exception:
                logger.exception("Unexpected error during reservation attempt")

            time.sleep(random.uniform(self.config.check_interval_min, self.config.check_interval_max))
