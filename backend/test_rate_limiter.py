from rate_limiter import check_rate_limit, submission_log


def test_rate_limit_allows_first_five_submissions():
    ip_address = "192.168.1.100"

    submission_log.pop(ip_address, None)

    for _ in range(5):
        result = check_rate_limit(ip_address)
        assert result["is_rate_limited"] is False

    assert result["submission_count"] == 5


def test_rate_limit_blocks_sixth_submission():
    ip_address = "192.168.1.101"

    submission_log.pop(ip_address, None)

    for _ in range(5):
        check_rate_limit(ip_address)

    result = check_rate_limit(ip_address)

    assert result["is_rate_limited"] is True
    assert result["submission_count"] == 5