import csv
from pathlib import Path

from backend.services.perplexity_analyzer import (
    calculate_perplexity,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_FILE = (
    PROJECT_ROOT
    / "data"
    / "training"
    / "verified_cv_dataset.csv"
)


def main():
    samples = []

    print("Loading dataset and calculating perplexity...")

    with DATASET_FILE.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            label = row["label"]

            if label not in {
                "human",
                "ai_generated",
            }:
                continue

            text = row["Text"].strip()

            if not text:
                continue

            result = calculate_perplexity(text)

            perplexity = result.get("perplexity")

            if perplexity is None:
                continue

            actual = 1 if label == "ai_generated" else 0

            samples.append(
                {
                    "perplexity": perplexity,
                    "actual": actual,
                }
            )

    print()
    print("=" * 65)
    print("Perplexity Threshold Evaluation")
    print("=" * 65)

    print(f"Samples evaluated: {len(samples)}")

    thresholds = [
        25,
        30,
        35,
        40,
        45,
        50,
        60,
        75,
        100,
        150,
        250,
        500,
    ]

    print()
    print(
        f"{'Threshold':<12}"
        f"{'Accuracy':<12}"
        f"{'False Pos.':<12}"
        f"{'False Neg.':<12}"
    )

    print("-" * 48)

    for threshold in thresholds:

        true_positive = 0
        true_negative = 0
        false_positive = 0
        false_negative = 0

        for sample in samples:

            predicted = (
                1
                if sample["perplexity"] <= threshold
                else 0
            )

            actual = sample["actual"]

            if predicted == 1 and actual == 1:
                true_positive += 1

            elif predicted == 0 and actual == 0:
                true_negative += 1

            elif predicted == 1 and actual == 0:
                false_positive += 1

            elif predicted == 0 and actual == 1:
                false_negative += 1

        total = len(samples)

        accuracy = (
            (true_positive + true_negative)
            / total
            if total
            else 0
        )

        print(
            f"{threshold:<12}"
            f"{accuracy:.2%}"
            f"{'':<6}"
            f"{false_positive:<12}"
            f"{false_negative:<12}"
        )

    print()
    print(
        "Interpretation:"
    )
    print(
        "Lower perplexity is treated as a possible AI-content signal."
    )
    print(
        "This evaluation is dataset-specific and does not prove"
    )
    print(
        "that a threshold will generalize to all resumes."
    )


if __name__ == "__main__":
    main()

    

    
    
    
    
    
    