def calculate_ai_risk(
    analysis: dict,
    metadata_analysis: dict | None = None,
) -> dict:
    """
    Calculate an AI-content risk score from multiple independent signals.

    Important:
    This is a heuristic risk model, not proof that a document was written by AI.
    Individual signals can also occur in legitimate human-written resumes.
    """

    score = 0
    signals = []
    contributions = []

    def add_signal(name: str, points: int) -> None:
        nonlocal score

        score += points

        signals.append(name)

        contributions.append({
            "signal": name,
            "points": points,
        })

    # ---------------------------------------------------------
    # Extract analysis features safely
    # ---------------------------------------------------------

    burstiness = float(analysis.get("burstiness", 0))
    buzzword_count = int(analysis.get("buzzword_count", 0))
    bigram_density = float(analysis.get("bigram_density", 0))
    trigram_density = float(analysis.get("trigram_density", 0))
    ai_style_pattern_count = int(
        analysis.get("ai_style_pattern_count", 0)
    )

    sentence_count = int(
        analysis.get("sentence_count", 0)
    )

    vocabulary_diversity = float(
        analysis.get("vocabulary_diversity", 0)
    )

    # ---------------------------------------------------------
    # 1. Sentence-length variation
    # ---------------------------------------------------------

    if sentence_count >= 5:
        if burstiness < 4:
            add_signal(
                "Low sentence-length variation",
                25,
            )
        elif burstiness < 6.5:
            add_signal(
                "Moderate sentence-length variation",
                10,
            )

    # ---------------------------------------------------------
    # 2. Repeated bigrams
    # ---------------------------------------------------------

    if bigram_density > 0.125:
        add_signal(
            "High repeated bigram density",
            15,
        )
    elif bigram_density > 0.075:
        add_signal(
            "Moderate repeated bigram density",
            8,
        )

    # ---------------------------------------------------------
    # 3. Repeated trigrams
    # ---------------------------------------------------------

    if trigram_density > 0.045:
        add_signal(
            "High repeated trigram density",
            10,
        )
    elif trigram_density > 0.02:
        add_signal(
            "Moderate repeated trigram density",
            5,
        )

    # ---------------------------------------------------------
    # 4. Generic AI-style phrases
    # ---------------------------------------------------------

    if buzzword_count >= 4:
        add_signal(
            "Multiple generic AI-style phrases",
            20,
        )
    elif buzzword_count >= 2:
        add_signal(
            "Some generic AI-style phrases",
            10,
        )
    elif buzzword_count == 1:
        add_signal(
            "One generic AI-style phrase",
            5,
        )

    # ---------------------------------------------------------
    # 5. Corporate / AI-style linguistic patterns
    # ---------------------------------------------------------

    if ai_style_pattern_count >= 4:
        add_signal(
            "Multiple generic corporate/AI-style patterns",
            15,
        )
    elif ai_style_pattern_count >= 2:
        add_signal(
            "Some generic corporate/AI-style patterns",
            10,
        )
    elif ai_style_pattern_count == 1:
        add_signal(
            "One generic corporate/AI-style pattern",
            5,
        )

    # ---------------------------------------------------------
    # 6. Vocabulary diversity
    #
    # Low diversity can be a supporting signal, but we keep
    # its weight small because short resumes naturally repeat
    # important technical/job-related terms.
    # ---------------------------------------------------------

    if sentence_count >= 8:
        if vocabulary_diversity < 0.45:
            add_signal(
                "Low vocabulary diversity",
                5,
            )

    # ---------------------------------------------------------
    # 7. Document metadata
    # ---------------------------------------------------------

    if metadata_analysis:
        suspicious_count = int(
            metadata_analysis.get(
                "suspicious_count",
                0,
            )
        )

        if suspicious_count > 0:
            add_signal(
                "Suspicious document metadata",
                10,
            )

    # ---------------------------------------------------------
    # Final score
    # ---------------------------------------------------------

    score = min(score, 100)

    # ---------------------------------------------------------
    # Classification
    # ---------------------------------------------------------

    if score > 65:
        classification = "High AI-content risk"
    elif score > 35:
        classification = "Moderate AI-content risk"
    else:
        classification = "Low AI-content risk"

    return {
        "ai_risk_score": score,
        "classification": classification,
        "signals": signals,
        "contributions": contributions,
    }