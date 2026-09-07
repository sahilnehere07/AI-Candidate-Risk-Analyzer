from pathlib import Path

from services.metadata_analyzer import extract_pdf_metadata


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = PROJECT_ROOT / "AI_Resume_Detector_Project_Guide.pdf"


def test_extract_pdf_metadata():
    metadata = extract_pdf_metadata(str(PDF_PATH))

    assert isinstance(metadata, dict)
    assert "author" in metadata
    assert "creator" in metadata
    assert "producer" in metadata