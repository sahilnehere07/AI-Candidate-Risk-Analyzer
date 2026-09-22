from pathlib import Path

from backend.services.candidate_analysis import (
    analyze_candidate_document,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def main():
    files = sorted(
        list(DATA_DIR.glob("ai_*.txt"))
        + list(DATA_DIR.glob("human_*.txt"))
    )

    print("=" * 50)
    print("Full Candidate Risk Pipeline Test")
    print("=" * 50)

    if not files:
        print("No local AI/human TXT files found.")
        return

    for file_path in files:

        text = file_path.read_bytes()

        result = analyze_candidate_document(
            text,
            file_path.name,
        )

        risk = result["risk"]

        print()
        print(file_path.name)
        print("-" * 40)
        print(
            f"ML AI probability: "
            f"{risk['ml_ai_probability']:.2%}"
        )
        print(
            f"Combined AI risk: "
            f"{risk['ai_risk_score']}/100"
        )
        print(
            f"Classification: "
            f"{risk['classification']}"
        )
        print(
            f"Signals: "
            f"{len(risk['signals'])}"
        )


if __name__ == "__main__":
    main()