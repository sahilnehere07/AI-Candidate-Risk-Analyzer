import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from bot_detector import detect_bot


def test_normal_human_submission():
    result = detect_bot(
        honeypot_value="",
        time_taken_seconds=10,
        user_agent="Mozilla/5.0",
    )

    assert result["is_bot"] is False
    assert result["reason_count"] == 0
    assert result["reasons"] == []


def test_too_fast_submission():
    result = detect_bot(
        honeypot_value="",
        time_taken_seconds=1,
        user_agent="Mozilla/5.0",
    )

    assert result["is_bot"] is True
    assert "Submission was completed too quickly" in result["reasons"]


def test_suspicious_user_agent():
    result = detect_bot(
        honeypot_value="",
        time_taken_seconds=10,
        user_agent="Puppeteer HeadlessChrome",
    )

    assert result["is_bot"] is True
    assert any("puppeteer" in reason.lower() for reason in result["reasons"])
    assert any("headless" in reason.lower() for reason in result["reasons"])


def test_honeypot():
    result = detect_bot(
        honeypot_value="spam-filled-value",
        time_taken_seconds=10,
        user_agent="Mozilla/5.0",
    )

    assert result["is_bot"] is True