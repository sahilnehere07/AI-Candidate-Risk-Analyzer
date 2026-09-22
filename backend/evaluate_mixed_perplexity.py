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
    perplexities = []

    with DATASET_FILE.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["label"] != "mixed":
                continue

            text = row["Text"].strip()

            if not text:
                continue

            result = calculate_perplexity(text)

            value = result.get("perplexity")

            if value is not None:
                perplexities.append(value)

    print("=" * 50)
    print("Mixed CV Perplexity Evaluation")
    print("=" * 50)

    print()
    print(f"Mixed CVs evaluated: {len(perplexities)}")

    if not perplexities:
        print("No perplexity values available.")
        return

    print(
        f"Average perplexity: "
        f"{sum(perplexities) / len(perplexities):.2f}"
    )

    print(
        f"Minimum perplexity: "
        f"{min(perplexities):.2f}"
    )

    print(
        f"Maximum perplexity: "
        f"{max(perplexities):.2f}"
    )

    # Count how many mixed CVs fall into useful ranges.
    below_40 = sum(
        value <= 40
        for value in perplexities
    )

    between_40_100 = sum(
        40 < value <= 100
        for value in perplexities
    )

    above_100 = sum(
        value > 100
        for value in perplexities
    )

    print()
    print("Perplexity ranges:")
    print(f"<= 40: {below_40}")
    print(f"40-100: {between_40_100}")
    print(f"> 100: {above_100}")

    print()
    print(
        "Mixed CVs do not have a binary Human/AI ground truth."
    )
    print(
        "Therefore, accuracy is not calculated."
    )


if __name__ == "__main__":
    main()