from services.candidate_risk import build_candidate_risk


def test_candidate_risk_combines_results():
    ai_risk = {
        "ai_risk_score": 43,
        "classification": "Moderate AI-content risk",
        "signals": [
            "Low sentence-length variation"
        ],
    }

    bot_detection = {
        "is_bot": True,
        "reason_count": 2,
        "reasons": [
            "Honeypot field was filled",
            "Submission was completed too quickly",
        ],
    }

    result = build_candidate_risk(
        ai_risk=ai_risk,
        bot_detection=bot_detection,
    )

    assert result["ai_content"]["score"] == 43
    assert result["ai_content"]["classification"] == "Moderate AI-content risk"

    assert result["bot_behavior"]["is_bot"] is True
    assert result["bot_behavior"]["reason_count"] == 2
    assert len(result["bot_behavior"]["reasons"]) == 2