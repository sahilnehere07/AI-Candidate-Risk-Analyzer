from pathlib import Path

from backend.services.perplexity_analyzer import (
    calculate_perplexity,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def main():
    files = sorted(
        list(DATA_DIR.glob("ai_*.txt"))
        + list(DATA_DIR.glob("human_*.txt"))
    )

    print("=" * 50)
    print("Perplexity Evaluation")
    print("=" * 50)

    if not files:
        print("No local evaluation files found.")
        return

    for file_path in files:

        text = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        ).strip()

        result = calculate_perplexity(text)

        print()
        print(file_path.name)
        print("-" * 40)
        print(
            f"Perplexity: "
            f"{result.get('perplexity')}"
        )
        print(
            f"Available: "
            f"{result.get('perplexity_available')}"
        )


if __name__ == "__main__":
    main()