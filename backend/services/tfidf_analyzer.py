from sklearn.feature_extraction.text import TfidfVectorizer


def analyze_with_tfidf(text: str) -> dict:
    """
    Extract TF-IDF based features from candidate text.

    TF-IDF measures how important words are within the document.
    It is a supporting NLP feature, not proof of AI-generated text.
    """

    if not text or not text.strip():
        return {
            "tfidf_feature_count": 0,
            "tfidf_average_weight": 0.0,
            "tfidf_max_weight": 0.0,
        }

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        max_features=500,
    )

    try:
        matrix = vectorizer.fit_transform([text])
    except ValueError:
        return {
            "tfidf_feature_count": 0,
            "tfidf_average_weight": 0.0,
            "tfidf_max_weight": 0.0,
        }

    weights = matrix.toarray()[0]

    non_zero_weights = [
        float(weight)
        for weight in weights
        if weight > 0
    ]

    if not non_zero_weights:
        return {
            "tfidf_feature_count": 0,
            "tfidf_average_weight": 0.0,
            "tfidf_max_weight": 0.0,
        }

    return {
        "tfidf_feature_count": len(non_zero_weights),
        "tfidf_average_weight": round(
            sum(non_zero_weights) / len(non_zero_weights),
            4,
        ),
        "tfidf_max_weight": round(
            max(non_zero_weights),
            4,
        ),
    }