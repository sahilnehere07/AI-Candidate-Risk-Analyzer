from evaluator import evaluate_dataset


def test_evaluation_dataset():
    result = evaluate_dataset()

    assert len(result["results"]) == 6

    assert result["true_positive"] >= 1
    assert result["true_negative"] >= 1

    assert result["false_positive"] >= 0
    assert result["false_negative"] >= 0

    assert 0 <= result["accuracy"] <= 1
    assert 0 <= result["precision"] <= 1
    assert 0 <= result["recall"] <= 1