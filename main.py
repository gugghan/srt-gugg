import argparse
import logging
import os

from srt_bot.bot import SRTBot
from srt_bot.config import Config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SRT 자동 예매 봇")
    parser.add_argument("--dep", help="출발역 (예: 수서)")
    parser.add_argument("--arr", help="도착역 (예: 부산)")
    parser.add_argument("--date", help="예매 날짜 YYYYMMDD")
    parser.add_argument("--time-start", help="검색 시작 시간 HHMMSS")
    parser.add_argument("--time-end", help="검색 종료 시간 HHMMSS")
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    args = parse_args()
    config = Config.from_env()

    if args.dep:
        config.dep_station = args.dep
    if args.arr:
        config.arr_station = args.arr
    if args.date:
        config.date = args.date
    if args.time_start:
        config.time_start = args.time_start
    if args.time_end:
        config.time_end = args.time_end

    bot = SRTBot(config)
    reserved = bot.run()

    github_output = os.getenv("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"reserved={'true' if reserved else 'false'}\n")


if __name__ == "__main__":
    main()
