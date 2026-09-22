from pathlib import Path
import csv

from backend.services.candidate_analysis import (
    analyze_candidate_document,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "data" / "evaluation"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(
        list(DATA_DIR.glob("ai_*.txt"))
        + list(DATA_DIR.glob("human_*.txt"))
    )

    if not files:
        print("No local evaluation files found.")
        return

    results = []

    for file_path in files:

        result = analyze_candidate_document(
            file_path.read_bytes(),
            file_path.name,
        )

        risk = result["risk"]

        actual_label = (
            "AI-generated"
            if file_path.name.lower().startswith("ai_")
            else "Human"
        )

        results.append({
            "filename": file_path.name,
            "actual_label": actual_label,
            "ml_ai_probability": risk["ml_ai_probability"],
            "combined_ai_risk": risk["ai_risk_score"],
            "classification": risk["classification"],
            "signal_count": len(risk["signals"]),
        })

    output_file = OUTPUT_DIR / "full_pipeline_report.csv"

    with output_file.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "filename",
                "actual_label",
                "ml_ai_probability",
                "combined_ai_risk",
                "classification",
                "signal_count",
            ],
        )

        writer.writeheader()
        writer.writerows(results)

    print("=" * 50)
    print("Evaluation report created")
    print("=" * 50)
    print(f"Files evaluated: {len(results)}")
    print(f"Report: {output_file}")


if __name__ == "__main__":
    main()