from services.risk_scorer import calculate_ai_risk


def test_low_ai_risk():
    analysis = {
        "burstiness": 10.0,
        "buzzword_count": 0,
        "bigram_density": 0.01,
        "trigram_density": 0.005,
    }

    result = calculate_ai_risk(analysis)

    assert result["ai_risk_score"] == 0
    assert result["classification"] == "Low AI-content risk"
    assert result["signals"] == []
    assert result["contributions"] == []


def test_high_ai_signals():
    analysis = {
        "burstiness": 2.0,
        "buzzword_count": 4,
        "bigram_density": 0.13,
        "trigram_density": 0.05,
    }

    result = calculate_ai_risk(analysis)

    assert result["ai_risk_score"] == 70
    assert result["classification"] == "High AI-content risk"

    assert len(result["signals"]) == 4
    assert len(result["contributions"]) == 4

    total_points = sum(
        item["points"]
        for item in result["contributions"]
    )

    assert total_points == 70


def test_suspicious_metadata_adds_risk():
    analysis = {
        "burstiness": 10.0,
        "buzzword_count": 0,
        "bigram_density": 0.01,
        "trigram_density": 0.005,
    }

    metadata_analysis = {
        "suspicious_count": 1,
        "suspicious_fields": [
            {
                "field": "creator",
                "value": "ChatGPT",
                "reason": "Contains suspicious tool name: chatgpt",
            }
        ],
    }

    result = calculate_ai_risk(
        analysis,
        metadata_analysis,
    )

    assert result["ai_risk_score"] == 10
    assert result["classification"] == "Low AI-content risk"

    assert "Suspicious document metadata" in (
        result["signals"]
    )

    assert result["contributions"] == [
        {
            "signal": "Suspicious document metadata",
            "points": 10,
        }
    ]


def test_trigram_density_adds_risk():
    analysis = {
        "burstiness": 10.0,
        "buzzword_count": 0,
        "bigram_density": 0.01,
        "trigram_density": 0.05,
    }

    result = calculate_ai_risk(analysis)

    assert result["ai_risk_score"] == 10
    assert result["classification"] == "Low AI-content risk"

    assert "High repeated trigram density" in (
        result["signals"]
    )

    assert result["contributions"] == [
        {
            "signal": "High repeated trigram density",
            "points": 10,
        }
    ]


def test_normal_repetition_is_not_high_risk():
    analysis = {
        "burstiness": 20.0,
        "buzzword_count": 0,
        "bigram_density": 0.1077,
        "trigram_density": 0.0338,
    }

    result = calculate_ai_risk(analysis)

    assert result["ai_risk_score"] == 13
    assert result["classification"] == "Low AI-content risk"

    assert result["signals"] == [
        "Moderate repeated bigram density",
        "Moderate repeated trigram density",
    ]


def test_ai_style_features_produce_higher_score():
    analysis = {
        "burstiness": 3.62,
        "buzzword_count": 2,
        "bigram_density": 0.1419,
        "trigram_density": 0.0544,
    }

    result = calculate_ai_risk(analysis)

    assert result["ai_risk_score"] == 60
    assert result["classification"] == "Moderate AI-content risk"

    assert "Low sentence-length variation" in (
        result["signals"]
    )

    assert "High repeated bigram density" in (
        result["signals"]
    )

    assert "High repeated trigram density" in (
        result["signals"]
    )

    assert "Some generic AI-style phrases" in (
        result["signals"]
    )