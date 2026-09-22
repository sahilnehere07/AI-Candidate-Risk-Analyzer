from pathlib import Path

import joblib


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

MODEL_DIR = PROJECT_ROOT / "data" / "ml_model"

VECTORIZER_PATH = MODEL_DIR / "tfidf_vectorizer.joblib"
MODEL_PATH = MODEL_DIR / "ai_text_classifier.joblib"


def main() -> None:
    vectorizer = joblib.load(
        VECTORIZER_PATH
    )

    model = joblib.load(
        MODEL_PATH
    )

    files = sorted(
        list(DATA_DIR.glob("ai_*.txt"))
        + list(DATA_DIR.glob("human_*.txt"))
    )

    print()
    print("========================================")
    print("External Local CV Sanity Test")
    print("========================================")
    print()

    if not files:
        print("No local AI/human TXT files found.")
        return

    correct = 0

    for file_path in files:

        text = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        ).strip()

        if not text:
            continue

        features = vectorizer.transform(
            [text]
        )

        prediction = model.predict(
            features
        )[0]

        probability = model.predict_proba(
            features
        )[0][1]

        actual = (
            1
            if file_path.name.lower().startswith("ai_")
            else 0
        )

        predicted_name = (
            "AI-generated"
            if prediction == 1
            else "Human"
        )

        actual_name = (
            "AI-generated"
            if actual == 1
            else "Human"
        )

        is_correct = prediction == actual

        if is_correct:
            correct += 1

        print(
            f"{file_path.name}: "
            f"Actual={actual_name}, "
            f"Predicted={predicted_name}, "
            f"AI probability={probability:.2%}"
        )

    print()
    print(
        f"Correct: {correct}/{len(files)}"
    )

    print(
        f"External sanity accuracy: "
        f"{correct / len(files):.2%}"
    )

    print()
    print(
        "This is a small external sanity check, "
        "not a statistically strong accuracy estimate."
    )


if __name__ == "__main__":
    main()