from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.services.text_analyzer import analyze_sentences
from backend.services.risk_scorer import calculate_ai_risk


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


DATASETS = {
    "Controlled dataset": [
        ("ai_resume.pdf", "AI-style"),
        ("ai_resume_2.txt", "AI-style"),
        ("ai_resume_3.txt", "AI-style"),
        ("human_resume.pdf.pdf", "Human"),
        ("human_resume_2.txt", "Human"),
        ("human_resume_3.txt", "Human"),
    ],
    "Adversarial human dataset": [
        ("human_edge_corporate.txt", "Human"),
        ("human_edge_technical.txt", "Human"),
        ("human_edge_uniform.txt", "Human"),
    ],
}


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()

    if suffix == ".txt":
        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    if suffix == ".pdf":
        import pdfplumber

        with pdfplumber.open(path) as pdf:
            pages = []

            for page in pdf.pages:
                text = page.extract_text()

                if text:
                    pages.append(text)

            return "\n".join(pages)

    raise ValueError(f"Unsupported file: {path.name}")


def predict(text: str) -> tuple[str, int]:
    analysis = analyze_sentences(text)

    risk = calculate_ai_risk(analysis)

    score = risk["ai_risk_score"]

    prediction = "AI-style" if score > 35 else "Human"

    return prediction, score


def calculate_metrics(results: list[tuple[str, str, str, int]]) -> dict:
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    for _, expected, predicted, _ in results:
        if expected == "AI-style" and predicted == "AI-style":
            true_positive += 1

        elif expected == "Human" and predicted == "Human":
            true_negative += 1

        elif expected == "Human" and predicted == "AI-style":
            false_positive += 1

        elif expected == "AI-style" and predicted == "Human":
            false_negative += 1

    total = (
        true_positive
        + true_negative
        + false_positive
        + false_negative
    )

    accuracy = (
        (true_positive + true_negative) / total
        if total
        else 0
    )

    precision = (
        true_positive / (true_positive + false_positive)
        if true_positive + false_positive
        else 0
    )

    recall = (
        true_positive / (true_positive + false_negative)
        if true_positive + false_negative
        else 0
    )

    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0
    )

    return {
        "tp": true_positive,
        "tn": true_negative,
        "fp": false_positive,
        "fn": false_negative,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def print_metrics(metrics: dict) -> None:
    print(f"TP        : {metrics['tp']}")
    print(f"TN        : {metrics['tn']}")
    print(f"FP        : {metrics['fp']}")
    print(f"FN        : {metrics['fn']}")
    print(f"Accuracy  : {metrics['accuracy']:.3f}")
    print(f"Precision : {metrics['precision']:.3f}")
    print(f"Recall    : {metrics['recall']:.3f}")
    print(f"F1 Score  : {metrics['f1']:.3f}")


def main():
    all_results = []

    print("\nAI Candidate Risk Analyzer")
    print("=" * 75)

    for dataset_name, dataset in DATASETS.items():
        print(f"\n{dataset_name}")
        print("-" * 75)

        dataset_results = []

        for filename, expected in dataset:
            path = DATA_DIR / filename

            if not path.exists():
                print(f"MISSING: {filename}")
                continue

            text = extract_text(path)

            predicted, score = predict(text)

            result = (
                filename,
                expected,
                predicted,
                score,
            )

            dataset_results.append(result)
            all_results.append(result)

            print(
                f"{filename:<30}"
                f" expected={expected:<10}"
                f" predicted={predicted:<10}"
                f" score={score}"
            )

        metrics = calculate_metrics(dataset_results)

        print("\nGroup metrics:")
        print_metrics(metrics)

    overall_metrics = calculate_metrics(all_results)

    print("\n" + "=" * 75)
    print("OVERALL RESULTS")
    print("=" * 75)

    print_metrics(overall_metrics)

    print("\nNote:")
    print(
        "These metrics describe this controlled evaluation dataset only. "
        "They do not represent universal real-world AI detection accuracy."
    )


if __name__ == "__main__":
    main()