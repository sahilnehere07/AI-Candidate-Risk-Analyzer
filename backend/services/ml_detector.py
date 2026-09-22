from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


MODEL_DIR = (
    Path(__file__).resolve().parent.parent.parent
    / "models"
)

VECTORIZER_PATH = MODEL_DIR / "tfidf_vectorizer.joblib"
MODEL_PATH = MODEL_DIR / "ai_text_classifier.joblib"

_vectorizer = None
_model = None


def train_model(
    texts: list[str],
    labels: list[int],
) -> dict:
    """
    Train a TF-IDF + Logistic Regression classifier.

    labels:
        0 = human-written
        1 = AI-generated
    """

    if len(texts) != len(labels):
        raise ValueError(
            "Texts and labels must have the same length."
        )

    if len(texts) < 10:
        raise ValueError(
            "At least 10 labelled examples are required."
        )

    if len(set(labels)) < 2:
        raise ValueError(
            "Training data must contain both human and AI examples."
        )

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000,
        sublinear_tf=True,
    )

    features = vectorizer.fit_transform(texts)

    model = LogisticRegression(
        max_iter=1000,
        random_state=42,
    )

    model.fit(
        features,
        labels,
    )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        vectorizer,
        VECTORIZER_PATH,
    )

    joblib.dump(
        model,
        MODEL_PATH,
    )

    global _vectorizer
    global _model

    _vectorizer = vectorizer
    _model = model

    return {
        "training_samples": len(texts),
        "feature_count": features.shape[1],
        "model": "Logistic Regression",
        "vectorizer": "TF-IDF",
        "model_path": str(MODEL_PATH),
        "vectorizer_path": str(VECTORIZER_PATH),
    }


def _load_model():
    """
    Load the trained model and vectorizer once
    and reuse them for subsequent predictions.
    """

    global _vectorizer
    global _model

    if _vectorizer is not None and _model is not None:
        return _vectorizer, _model

    if not MODEL_PATH.exists() or not VECTORIZER_PATH.exists():
        return None, None

    _vectorizer = joblib.load(
        VECTORIZER_PATH
    )

    _model = joblib.load(
        MODEL_PATH
    )

    return _vectorizer, _model


def predict_ai_probability(
    text: str,
) -> dict:
    """
    Predict the probability that text belongs to
    the AI-generated class.

    Returns a probability from 0 to 1.
    """

    if not text or not text.strip():
        return {
            "ai_probability": 0.0,
            "ml_available": False,
        }

    vectorizer, model = _load_model()

    if vectorizer is None or model is None:
        return {
            "ai_probability": 0.0,
            "ml_available": False,
        }

    features = vectorizer.transform(
        [text]
    )

    probability = model.predict_proba(
        features
    )[0][1]

    return {
        "ai_probability": round(
            float(probability),
            4,
        ),
        "ml_available": True,
    }