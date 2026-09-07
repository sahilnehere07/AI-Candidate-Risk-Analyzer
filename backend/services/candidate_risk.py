def build_candidate_risk(
    ai_risk: dict,
    bot_detection: dict,
    rate_limit: dict | None = None,
) -> dict:
    bot_risk = {
        "is_bot": bot_detection["is_bot"],
        "reason_count": bot_detection["reason_count"],
        "reasons": bot_detection["reasons"],
    }

    if rate_limit is not None:
        bot_risk["rate_limited"] = (
            rate_limit["is_rate_limited"]
        )

    if ai_risk["ai_risk_score"] > 65:
        overall_status = "High Risk"
    elif (
        ai_risk["ai_risk_score"] > 35
        or bot_detection["is_bot"]
    ):
        overall_status = "Review"
    else:
        overall_status = "Low Risk"

    return {
        "overall_status": overall_status,
        "ai_content": {
            "score": ai_risk["ai_risk_score"],
            "classification": ai_risk["classification"],
            "signals": ai_risk["signals"],
            "contributions": ai_risk.get(
                "contributions",
                [],
            ),
        },
        "bot_behavior": bot_risk,
    }