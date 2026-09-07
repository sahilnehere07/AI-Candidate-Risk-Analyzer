from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == (
        "AI Candidate Risk Analyzer backend is running"
    )


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_candidate_risk_low_risk():
    response = client.post(
        "/candidate-risk",
        json={
            "ai_risk": {
                "ai_risk_score": 20,
                "classification": "Low AI-content risk",
                "signals": [],
                "contributions": [],
            },
            "bot_detection": {
                "is_bot": False,
                "reason_count": 0,
                "reasons": [],
            },
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["overall_status"] == "Low Risk"
    assert data["ai_content"]["score"] == 20
    assert data["bot_behavior"]["is_bot"] is False


def test_candidate_risk_ai_review():
    response = client.post(
        "/candidate-risk",
        json={
            "ai_risk": {
                "ai_risk_score": 50,
                "classification": "Moderate AI-content risk",
                "signals": [
                    "Low sentence-length variation",
                ],
                "contributions": [],
            },
            "bot_detection": {
                "is_bot": False,
                "reason_count": 0,
                "reasons": [],
            },
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["overall_status"] == "Review"


def test_candidate_risk_bot_review():
    response = client.post(
        "/candidate-risk",
        json={
            "ai_risk": {
                "ai_risk_score": 10,
                "classification": "Low AI-content risk",
                "signals": [],
                "contributions": [],
            },
            "bot_detection": {
                "is_bot": True,
                "reason_count": 1,
                "reasons": [
                    "Honeypot field was filled",
                ],
            },
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["overall_status"] == "Review"
    assert data["bot_behavior"]["is_bot"] is True


def test_candidate_risk_rejects_missing_ai_risk():
    response = client.post(
        "/candidate-risk",
        json={
            "bot_detection": {
                "is_bot": False,
                "reason_count": 0,
                "reasons": [],
            },
        },
    )

    assert response.status_code == 422


def test_candidate_risk_rejects_invalid_ai_score():
    response = client.post(
        "/candidate-risk",
        json={
            "ai_risk": {
                "ai_risk_score": "not-a-number",
                "classification": "Low AI-content risk",
                "signals": [],
                "contributions": [],
            },
            "bot_detection": {
                "is_bot": False,
                "reason_count": 0,
                "reasons": [],
            },
        },
    )

    assert response.status_code == 422