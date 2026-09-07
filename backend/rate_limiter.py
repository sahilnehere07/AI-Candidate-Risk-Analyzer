import time


submission_log = {}

MAX_SUBMISSIONS = 5
WINDOW_SECONDS = 60


def check_rate_limit(ip_address: str) -> dict:

    current_time = time.time()

    if ip_address not in submission_log:
        submission_log[ip_address] = []

    # Keep only submissions from the last 60 seconds
    submission_log[ip_address] = [
        timestamp
        for timestamp in submission_log[ip_address]
        if current_time - timestamp < WINDOW_SECONDS
    ]

    submission_count = len(submission_log[ip_address])

    is_rate_limited = submission_count >= MAX_SUBMISSIONS

    if not is_rate_limited:
        submission_log[ip_address].append(current_time)

    return {
        "ip_address": ip_address,
        "submission_count": submission_count + 1
        if not is_rate_limited
        else submission_count,
        "is_rate_limited": is_rate_limited,
        "limit": MAX_SUBMISSIONS,
        "window_seconds": WINDOW_SECONDS,
    }