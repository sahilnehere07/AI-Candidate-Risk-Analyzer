from services.text_analyzer import (
    analyze_sentences,
    calculate_vocabulary_diversity,
    calculate_ngram_density,
)


def test_basic_text_analysis():
    text = (
        "I built a backend service. "
        "I tested the API thoroughly."
    )

    result = analyze_sentences(text)

    assert result["sentence_count"] == 2
    assert result["average_sentence_length"] > 0
    assert result["burstiness"] >= 0
    assert result["buzzword_count"] == 0


def test_ai_phrase_detection():
    text = (
        "I spearheaded cross-functional initiatives "
        "and leveraged cutting-edge solutions."
    )

    result = analyze_sentences(text)

    assert result["buzzword_count"] == 2
    assert (
        "spearheaded cross-functional initiatives"
        in result["flagged_phrases"]
    )


def test_ai_style_pattern_detection():
    text = (
        "Demonstrated exceptional ability to "
        "foster collaborative innovation and "
        "maximize business value."
    )

    result = analyze_sentences(text)

    assert result["ai_style_pattern_count"] >= 2


def test_vocabulary_diversity():
    text = "python python api database"

    diversity = calculate_vocabulary_diversity(text)

    assert diversity == 0.75


def test_repeated_ngrams_increase_density():
    repeated_text = (
        "python api python api python api"
    )

    normal_text = (
        "python api database testing frontend backend"
    )

    repeated_density = calculate_ngram_density(
        repeated_text,
        n=2,
    )

    normal_density = calculate_ngram_density(
        normal_text,
        n=2,
    )

    assert repeated_density > normal_density