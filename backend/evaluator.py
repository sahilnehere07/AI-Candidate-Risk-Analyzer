from pathlib import Path

from services.candidate_analysis import analyze_candidate_document


PROJECT_ROOT = Path(__file__).resolve().parent.parent


DATASET = [
    {
        "filename": "ai_resume.pdf",
        "path": PROJECT_ROOT / "data" / "ai_resume.pdf",
        "expected_label": "AI-style",
    },
    {
        "filename": "human_resume.pdf",
        "path": PROJECT_ROOT / "data" / "human_resume.pdf.pdf",
        "expected_label": "Human",
    },
    {
        "filename": "ai_resume_2.txt",
        "path": PROJECT_ROOT / "data" / "ai_resume_2.txt",
        "expected_label": "AI-style",
    },
    {
        "filename": "ai_resume_3.txt",
        "path": PROJECT_ROOT / "data" / "ai_resume_3.txt",
        "expected_label": "AI-style",
    },
    {
        "filename": "human_resume_2.txt",
        "path": PROJECT_ROOT / "data" / "human_resume_2.txt",
        "expected_label": "Human",
    },
    {
        "filename": "human_resume_3.txt",
        "path": PROJECT_ROOT / "data" / "human_resume_3.txt",
        "expected_label": "Human",
    },
]


def predict_label(result: dict) -> str:
    score = result["risk"]["ai_risk_score"]

    if score > 35:
        return "AI-style"

    return "Human"


def evaluate_dataset() -> dict:
    results = []

    for item in DATASET:
        file_content = item["path"].read_bytes()

        analysis_result = analyze_candidate_document(
            file_content=file_content,
            filename=item["filename"],
        )

        predicted_label = predict_label(
            analysis_result
        )

        results.append({
            "filename": item["filename"],
            "expected_label": item["expected_label"],
            "predicted_label": predicted_label,
            "score": analysis_result["risk"]["ai_risk_score"],
        })

    true_positive = sum(
        1
        for result in results
        if result["expected_label"] == "AI-style"
        and result["predicted_label"] == "AI-style"
    )

    true_negative = sum(
        1
        for result in results
        if result["expected_label"] == "Human"
        and result["predicted_label"] == "Human"
    )

    false_positive = sum(
        1
        for result in results
        if result["expected_label"] == "Human"
        and result["predicted_label"] == "AI-style"
    )

    false_negative = sum(
        1
        for result in results
        if result["expected_label"] == "AI-style"
        and result["predicted_label"] == "Human"
    )

    total = len(results)

    accuracy = (
        (true_positive + true_negative) / total
        if total
        else 0
    )

    precision = (
        true_positive / (true_positive + false_positive)
        if (true_positive + false_positive)
        else 0
    )

    recall = (
        true_positive / (true_positive + false_negative)
        if (true_positive + false_negative)
        else 0
    )

    return {
        "results": results,
        "true_positive": true_positive,
        "true_negative": true_negative,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
    }


if __name__ == "__main__":
    evaluation = evaluate_dataset()

    print("\nEvaluation Results")
    print("------------------")

    for result in evaluation["results"]:
        print(
            f"{result['filename']}: "
            f"expected={result['expected_label']}, "
            f"predicted={result['predicted_label']}, "
            f"score={result['score']}"
        )

    print()

    print(
        f"True positives:  "
        f"{evaluation['true_positive']}"
    )

    print(
        f"True negatives:  "
        f"{evaluation['true_negative']}"
    )

    print(
        f"False positives: "
        f"{evaluation['false_positive']}"
    )

    print(
        f"False negatives: "
        f"{evaluation['false_negative']}"
    )

    print(
        f"Accuracy:        "
        f"{evaluation['accuracy']}"
    )

    print(
        f"Precision:       "
        f"{evaluation['precision']}"
    )

    print(
        f"Recall:          "
        f"{evaluation['recall']}"
    )