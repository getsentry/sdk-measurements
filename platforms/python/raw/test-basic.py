import time
import os

import sentry_sdk


SENTRY_DSN = os.environ.get("SENTRY_DSN")
assert SENTRY_DSN, "SENTRY_DSN not provided!"

sentry_sdk.init(
    SENTRY_DSN,
    traces_sample_rate=0.0,
)


if __name__ == "__main__":
    time.sleep(1.0)
    print("Done!")
