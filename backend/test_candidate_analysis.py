from pathlib import Path

from services.candidate_analysis import analyze_candidate_document


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = PROJECT_ROOT / "data" / "ai_resume.pdf"


def test_candidate_analysis_pipeline():
    file_content = PDF_PATH.read_bytes()

    result = analyze_candidate_document(
        file_content=file_content,
        filename="ai_resume.pdf",
    )

    assert result["filename"] == "ai_resume.pdf"
    assert result["analysis"]["sentence_count"] > 0
    assert 0 <= result["risk"]["ai_risk_score"] <= 100
    assert "metadata" in result
    assert "metadata_analysis" in result