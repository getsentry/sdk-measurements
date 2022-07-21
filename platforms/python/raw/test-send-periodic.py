import logging
import time
import os
from datetime import datetime, timedelta
from typing import Callable

import sentry_sdk


SENTRY_DSN = os.environ.get("SENTRY_DSN")
assert SENTRY_DSN, "SENTRY_DSN not provided!"

sentry_sdk.init(
    SENTRY_DSN,
    traces_sample_rate=0.0,
)


def periodic_run(
    f: Callable, repetitions: int, period_seconds: int, total_seconds: int = 10
):
    """
    Call function `f` periodically: `repetitions` times every `period_seconds` period.
    Do it over the total period of `total_seconds`. If `total_seconds` is zero or negative,
    do it indefinitely.
    """
    start_time = datetime.now()

    if total_seconds > 0:
        end_time = start_time + timedelta(seconds=total_seconds)
    else:
        end_time = None

    # cur_period_start = start_time
    next_period_start = start_time + timedelta(seconds=period_seconds)
    repetitions_left = repetitions

    while 1:
        if end_time and datetime.now() > end_time:
            return

        f()

        repetitions_left -= 1
        now = datetime.now()

        if repetitions_left == 0:
            if now < next_period_start:
                delta = next_period_start - now
                logging.info("Waiting until next period...")
                time.sleep(delta.total_seconds())

            # cur_period_start = next_period_start
            next_period_start += timedelta(seconds=period_seconds)
            repetitions_left = repetitions
            continue
        else:
            # FIXME
            time.sleep(0.001)


def func():
    logging.info("Sending a message")
    sentry_sdk.capture_message("Something went wrong")


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    periodic_run(func, repetitions=3, period_seconds=1, total_seconds=60)
    sentry_sdk.flush()
    print("Done!")
