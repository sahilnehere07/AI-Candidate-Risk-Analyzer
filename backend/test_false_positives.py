from services.text_analyzer import analyze_sentences
from services.risk_scorer import calculate_ai_risk


def test_formal_human_style_is_not_automatically_high_risk():

    text = """
    I developed backend services using Python and FastAPI.
    I designed REST APIs for internal business applications.
    I implemented database integrations using PostgreSQL.
    I improved application performance through query optimization.
    I collaborated with engineers to resolve production issues.
    """

    analysis = analyze_sentences(text)

    result = calculate_ai_risk(analysis)

    assert result["ai_risk_score"] < 66