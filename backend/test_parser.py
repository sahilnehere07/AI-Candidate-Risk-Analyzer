from pathlib import Path

from services.document_parser import extract_text_from_pdf


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = PROJECT_ROOT / "AI_Resume_Detector_Project_Guide.pdf"


def test_extract_text_from_pdf():
    text = extract_text_from_pdf(str(PDF_PATH))

    assert text
    assert len(text) > 100
