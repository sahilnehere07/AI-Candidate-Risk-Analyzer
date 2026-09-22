def calculate_ai_risk(
    analysis: dict,
    metadata_analysis: dict | None = None,
) -> dict:
    """
    Calculate an AI-content risk score from multiple independent signals.

    Important:
    This is a heuristic risk model, not proof that a document was written by AI.
    Individual signals can also occur in legitimate human-written resumes.

    ML probability and perplexity are supporting signals only.
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

    burstiness = float(
        analysis.get("burstiness", 0)
    )

    buzzword_count = int(
        analysis.get("buzzword_count", 0)
    )

    bigram_density = float(
        analysis.get("bigram_density", 0)
    )

    trigram_density = float(
        analysis.get("trigram_density", 0)
    )

    ai_style_pattern_count = int(
        analysis.get("ai_style_pattern_count", 0)
    )

    sentence_count = int(
        analysis.get("sentence_count", 0)
    )

    vocabulary_diversity = float(
        analysis.get("vocabulary_diversity", 0)
    )

    ml_available = bool(
        analysis.get("ml_available", False)
    )

    ml_probability = float(
        analysis.get("ai_probability", 0)
    )

    perplexity_available = bool(
        analysis.get("perplexity_available", False)
    )

    perplexity = analysis.get(
        "perplexity"
    )

    if perplexity is not None:
        perplexity = float(perplexity)

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
    # ---------------------------------------------------------

    if sentence_count >= 8:

        if vocabulary_diversity < 0.45:

            add_signal(
                "Low vocabulary diversity",
                5,
            )

    # ---------------------------------------------------------
    # 7. ML text classifier
    #
    # Supporting signal only.
    # ---------------------------------------------------------

    if ml_available:

        if ml_probability >= 0.80:

            add_signal(
                "ML classifier indicates high AI probability",
                20,
            )

        elif ml_probability >= 0.60:

            add_signal(
                "ML classifier indicates moderate-high AI probability",
                12,
            )

        elif ml_probability >= 0.45:

            add_signal(
                "ML classifier indicates moderate AI probability",
                6,
            )

    # ---------------------------------------------------------
    # 8. Language-model perplexity
    #
    # Supporting signal only.
    #
    # These thresholds were selected from the current
    # evaluation experiments and should not be interpreted
    # as universal AI-detection thresholds.
    # ---------------------------------------------------------

    if perplexity_available and perplexity is not None:

        if perplexity <= 35:

            add_signal(
                "Very low language-model perplexity",
                15,
            )

        elif perplexity <= 50:

            add_signal(
                "Low language-model perplexity",
                5,
            )

    # ---------------------------------------------------------
    # 9. Document metadata
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

    # ---------------------------------------------------------
    # Return result
    # ---------------------------------------------------------

    return {
        "ai_risk_score": score,
        "classification": classification,
        "signals": signals,
        "contributions": contributions,
        "ml_available": ml_available,
        "ml_ai_probability": round(
            ml_probability,
            4,
        ),
        "perplexity_available": perplexity_available,
        "perplexity": perplexity,
    }