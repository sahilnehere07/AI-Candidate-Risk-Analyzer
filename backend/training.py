import csv
from pathlib import Path

import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent

TRAIN_FILE = (
    PROJECT_ROOT
    / "data"
    / "training"
    / "prepared"
    / "train.csv"
)

TEST_FILE = (
    PROJECT_ROOT
    / "data"
    / "training"
    / "prepared"
    / "test.csv"
)

MODEL_DIR = (
    PROJECT_ROOT
    / "data"
    / "ml_model"
)

VECTORIZER_PATH = (
    MODEL_DIR
    / "tfidf_vectorizer.joblib"
)

MODEL_PATH = (
    MODEL_DIR
    / "ai_text_classifier.joblib"
)


def load_csv(path: Path) -> tuple[list[str], list[int]]:
    texts = []
    labels = []

    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            text = row["text"].strip()

            if not text:
                continue

            texts.append(text)
            labels.append(int(row["label"]))

    return texts, labels


def main() -> None:
    print()
    print("========================================")
    print("AI CV Detection - ML Training")
    print("========================================")
    print()

    if not TRAIN_FILE.exists():
        raise FileNotFoundError(
            f"Training file not found: {TRAIN_FILE}"
        )

    if not TEST_FILE.exists():
        raise FileNotFoundError(
            f"Testing file not found: {TEST_FILE}"
        )

    X_train, y_train = load_csv(
        TRAIN_FILE
    )

    X_test, y_test = load_csv(
        TEST_FILE
    )

    print(
        f"Training samples: {len(X_train)}"
    )

    print(
        f"Testing samples:  {len(X_test)}"
    )

    print()

    # --------------------------------------------------
    # TF-IDF
    #
    # IMPORTANT:
    # fit_transform() is used ONLY on training data.
    # The test data is transformed using the same
    # vectorizer without learning from the test set.
    # --------------------------------------------------

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000,
        sublinear_tf=True,
    )

    X_train_features = vectorizer.fit_transform(
        X_train
    )

    X_test_features = vectorizer.transform(
        X_test
    )

    print(
        f"TF-IDF features: "
        f"{X_train_features.shape[1]}"
    )

    print()

    # --------------------------------------------------
    # Logistic Regression
    # --------------------------------------------------

    model = LogisticRegression(
        max_iter=1000,
        random_state=42,
    )

    model.fit(
        X_train_features,
        y_train,
    )

    # --------------------------------------------------
    # Test on unseen data
    # --------------------------------------------------

    predictions = model.predict(
        X_test_features
    )

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    matrix = confusion_matrix(
        y_test,
        predictions,
        labels=[0, 1],
    )

    print("========================================")
    print("MODEL EVALUATION")
    print("========================================")
    print()

    print(
        f"Accuracy: {accuracy:.2%}"
    )

    print()

    print("Classification report:")
    print(
        classification_report(
            y_test,
            predictions,
            labels=[0, 1],
            target_names=[
                "Human",
                "AI-generated",
            ],
            zero_division=0,
        )
    )

    print("Confusion matrix:")
    print(
        "                 Predicted Human  Predicted AI"
    )

    print(
        f"Actual Human       {matrix[0][0]:>6}"
        f"             {matrix[0][1]:>6}"
    )

    print(
        f"Actual AI          {matrix[1][0]:>6}"
        f"             {matrix[1][1]:>6}"
    )

    # --------------------------------------------------
    # Save trained model
    # --------------------------------------------------

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

    print()
    print("========================================")
    print("MODEL SAVED")
    print("========================================")
    print()
    print(
        f"Vectorizer: {VECTORIZER_PATH}"
    )
    print(
        f"Model:      {MODEL_PATH}"
    )
    print()
    print("Training completed successfully.")


if __name__ == "__main__":
    main()