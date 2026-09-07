def detect_bot(
    honeypot_value: str,
    time_taken_seconds: float,
    user_agent: str,
) -> dict:

    reasons = []

    # 1. Honeypot check
    if honeypot_value:
        reasons.append("Honeypot field was filled")

    # 2. Submission speed check
    if time_taken_seconds < 3:
        reasons.append("Submission was completed too quickly")

    # 3. User-agent check
    suspicious_agents = [
        "puppeteer",
        "selenium",
        "python-requests",
        "headless",
    ]

    user_agent_lower = user_agent.lower()

    for agent in suspicious_agents:
        if agent in user_agent_lower:
            reasons.append(
                f"Suspicious user-agent detected: {agent}"
            )

    return {
        "is_bot": len(reasons) > 0,
        "reason_count": len(reasons),
        "reasons": reasons,
    }