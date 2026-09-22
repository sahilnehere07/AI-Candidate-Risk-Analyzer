from pathlib import Path

from backend.services.perplexity_analyzer import (
    calculate_perplexity,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def calculate_perplexity_points(perplexity):
    if perplexity is None:
        return 0

    if perplexity <= 35:
        return 15

    if perplexity <= 50:
        return 5

    return 0


def main():
    files = sorted(
        list(DATA_DIR.glob("ai_*.txt"))
        + list(DATA_DIR.glob("human_*.txt"))
    )

    print("=" * 60)
    print("Revised Perplexity Risk Impact Test")
    print("=" * 60)

    for file_path in files:

        text = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        ).strip()

        result = calculate_perplexity(text)

        perplexity = result.get("perplexity")

        points = calculate_perplexity_points(
            perplexity
        )

        print()
        print(file_path.name)
        print("-" * 40)
        print(f"Perplexity: {perplexity}")
        print(f"Proposed points: +{points}")


if __name__ == "__main__":
    main()