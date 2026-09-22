import csv
from pathlib import Path

from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parent.parent

SOURCE_FILE = (
    PROJECT_ROOT
    / "data"
    / "training"
    / "verified_cv_dataset.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "training"
    / "prepared"
)


def load_dataset() -> list[dict]:
    records = []

    with SOURCE_FILE.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            label = row["label"]
            text = row["Text"].strip()

            # Use only human and AI-generated CVs.
            # Mixed CVs are reserved for later testing.
            if label not in {
                "human",
                "ai_generated",
            }:
                continue

            if not text:
                continue

            records.append({
                "text": text,
                "label": (
                    0
                    if label == "human"
                    else 1
                ),
                "original_label": label,
            })

    return records


def remove_duplicates(
    records: list[dict],
) -> list[dict]:
    seen = set()
    unique_records = []

    for record in records:
        normalized_text = " ".join(
            record["text"].lower().split()
        )

        if normalized_text in seen:
            continue

        seen.add(normalized_text)
        unique_records.append(record)

    return unique_records


def save_csv(
    records: list[dict],
    filename: str,
) -> None:

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = OUTPUT_DIR / filename

    with output_file.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "text",
                "label",
                "original_label",
            ],
        )

        writer.writeheader()

        for record in records:
            writer.writerow(record)


def main() -> None:

    print()
    print("========================================")
    print("Preparing AI CV Detection Dataset")
    print("========================================")
    print()

    records = load_dataset()

    print(
        f"Loaded human + AI CVs: {len(records)}"
    )

    records = remove_duplicates(records)

    print(
        f"After duplicate removal: {len(records)}"
    )

    texts = [
        record["text"]
        for record in records
    ]

    labels = [
        record["label"]
        for record in records
    ]

    X_train, X_test, y_train, y_test = (
        train_test_split(
            texts,
            labels,
            test_size=0.20,
            random_state=42,
            stratify=labels,
        )
    )

    train_records = [
        {
            "text": text,
            "label": label,
            "original_label": (
                "human"
                if label == 0
                else "ai_generated"
            ),
        }
        for text, label in zip(
            X_train,
            y_train,
        )
    ]

    test_records = [
        {
            "text": text,
            "label": label,
            "original_label": (
                "human"
                if label == 0
                else "ai_generated"
            ),
        }
        for text, label in zip(
            X_test,
            y_test,
        )
    ]

    save_csv(
        train_records,
        "train.csv",
    )

    save_csv(
        test_records,
        "test.csv",
    )

    print()
    print(
        f"Training samples: {len(train_records)}"
    )

    print(
        f"Testing samples:  {len(test_records)}"
    )

    print()
    print("Dataset preparation completed.")
    print()
    print(
        "Training file:"
        " data/training/prepared/train.csv"
    )

    print(
        "Testing file:"
        " data/training/prepared/test.csv"
    )


if __name__ == "__main__":
    main()