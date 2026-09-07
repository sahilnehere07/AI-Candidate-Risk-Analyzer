from pathlib import Path

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = PROJECT_ROOT / "data" / "ai_resume.pdf"


def test_upload_ai_resume_pdf():
    with open(PDF_PATH, "rb") as file:
        response = client.post(
            "/upload",
            files={
                "file": (
                    "ai_resume.pdf",
                    file,
                    "application/pdf",
                )
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "ai_resume.pdf"

    assert "analysis" in data
    assert "metadata" in data
    assert "metadata_analysis" in data
    assert "risk" in data

    assert data["analysis"]["sentence_count"] > 0

    assert 0 <= data["risk"]["ai_risk_score"] <= 100

    assert "contributions" in data["risk"]
    assert isinstance(
        data["risk"]["contributions"],
        list,
    )

    for contribution in data["risk"]["contributions"]:
        assert "signal" in contribution
        assert "points" in contribution


def test_upload_rejects_unsupported_file_type():
    response = client.post(
        "/upload",
        files={
            "file": (
                "resume.txt",
                b"some resume text",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "Only PDF and DOCX files are supported"
    )


def test_upload_rejects_empty_file():
    response = client.post(
        "/upload",
        files={
            "file": (
                "empty.pdf",
                b"",
                "application/pdf",
            )
        },
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "Uploaded file is empty"
    )


def test_upload_rejects_oversized_file():
    oversized_content = b"x" * (
        5 * 1024 * 1024 + 1
    )

    response = client.post(
        "/upload",
        files={
            "file": (
                "large.pdf",
                oversized_content,
                "application/pdf",
            )
        },
    )

    assert response.status_code == 413

    assert (
        response.json()["detail"]
        == "File size exceeds the 5 MB limit"
    )


def test_upload_rejects_corrupt_pdf():
    response = client.post(
        "/upload",
        files={
            "file": (
                "corrupt.pdf",
                b"This is not a real PDF file",
                "application/pdf",
            )
        },
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "Unable to process the uploaded document"
    )