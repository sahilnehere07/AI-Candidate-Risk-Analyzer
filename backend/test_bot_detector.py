from bot_detector import detect_bot


def test_normal_user_is_not_bot():
    result = detect_bot(
        honeypot_value="",
        time_taken_seconds=10,
        user_agent="Mozilla/5.0 Chrome",
    )

    assert result["is_bot"] is False
    assert result["reason_count"] == 0
    assert result["reasons"] == []


def test_suspicious_submission_is_bot():
    result = detect_bot(
        honeypot_value="I am a bot",
        time_taken_seconds=1,
        user_agent="Puppeteer Headless Chrome",
    )

    assert result["is_bot"] is True
    assert result["reason_count"] == 4
    assert "Honeypot field was filled" in result["reasons"]
    assert "Submission was completed too quickly" in result["reasons"]