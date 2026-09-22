import csv
from pathlib import Path

import joblib
from sklearn.metrics import classification_report


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_FILE = (
    PROJECT_ROOT
    / "data"
    / "training"
    / "verified_cv_dataset.csv"
)

MODEL_DIR = (
    PROJECT_ROOT
    / "data"
    / "ml_model"
)

VECTORIZER_PATH = MODEL_DIR / "tfidf_vectorizer.joblib"
MODEL_PATH = MODEL_DIR / "ai_text_classifier.joblib"


def load_mixed_cvs() -> list[str]:
    texts = []

    with DATASET_FILE.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["label"] == "mixed":
                text = row["Text"].strip()

                if text:
                    texts.append(text)

    return texts


def main() -> None:
    print()
    print("========================================")
    print("Mixed CV Robustness Evaluation")
    print("========================================")
    print()

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Trained ML model not found."
        )

    if not VECTORIZER_PATH.exists():
        raise FileNotFoundError(
            "TF-IDF vectorizer not found."
        )

    mixed_texts = load_mixed_cvs()

    print(
        f"Mixed CVs found: {len(mixed_texts)}"
    )

    vectorizer = joblib.load(
        VECTORIZER_PATH
    )

    model = joblib.load(
        MODEL_PATH
    )

    features = vectorizer.transform(
        mixed_texts
    )

    predictions = model.predict(
        features
    )

    probabilities = model.predict_proba(
        features
    )[:, 1]

    human_predictions = sum(
        prediction == 0
        for prediction in predictions
    )

    ai_predictions = sum(
        prediction == 1
        for prediction in predictions
    )

    average_ai_probability = (
        sum(probabilities)
        / len(probabilities)
    )

    print()
    print("Predictions on mixed CVs:")
    print(
        f"Predicted Human: {human_predictions}"
    )
    print(
        f"Predicted AI:    {ai_predictions}"
    )

    print()
    print(
        "Average AI probability:"
        f" {average_ai_probability:.2%}"
    )

    print()
    print(
        "Important:"
    )
    print(
        "Mixed CVs do not have a correct binary "
        "Human/AI label, so accuracy/F1 is NOT "
        "calculated for this experiment."
    )

    print()
    print(
        "This is a robustness analysis showing "
        "how the binary model behaves when a CV "
        "contains both human and AI-written content."
    )

    print()


if __name__ == "__main__":
    main()