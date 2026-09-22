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
    ai_scores = []
    human_scores = []

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

            if label == "ai_generated":
                ai_scores.append(perplexity)

            elif label == "human":
                human_scores.append(perplexity)

    print("=" * 50)
    print("Dataset Perplexity Evaluation")
    print("=" * 50)

    print()
    print(f"AI samples evaluated: {len(ai_scores)}")
    print(f"Human samples evaluated: {len(human_scores)}")

    if ai_scores:
        print()
        print(
            f"AI average perplexity: "
            f"{sum(ai_scores) / len(ai_scores):.2f}"
        )

        print(
            f"AI minimum perplexity: "
            f"{min(ai_scores):.2f}"
        )

        print(
            f"AI maximum perplexity: "
            f"{max(ai_scores):.2f}"
        )

    if human_scores:
        print()
        print(
            f"Human average perplexity: "
            f"{sum(human_scores) / len(human_scores):.2f}"
        )

        print(
            f"Human minimum perplexity: "
            f"{min(human_scores):.2f}"
        )

        print(
            f"Human maximum perplexity: "
            f"{max(human_scores):.2f}"
        )


if __name__ == "__main__":
    main()