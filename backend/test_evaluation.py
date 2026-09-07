from evaluator import evaluate_dataset


def test_evaluation_dataset():
    result = evaluate_dataset()

    assert len(result["results"]) == 6

    assert result["true_positive"] == 3
    assert result["true_negative"] == 3

    assert result["false_positive"] == 0
    assert result["false_negative"] == 0

    assert result["accuracy"] == 1.0
    assert result["precision"] == 1.0
    assert result["recall"] == 1.0