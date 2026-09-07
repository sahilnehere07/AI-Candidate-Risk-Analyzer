import pdfplumber
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def extract_text_from_docx(file_path: str) -> str:
    document = Document(file_path)

    text = []

    for paragraph in document.paragraphs:
        if paragraph.text:
            text.append(paragraph.text)

    return "\n".join(text)


def extract_text_from_txt(file_path: str) -> str:
    with open(
        file_path,
        "r",
        encoding="utf-8",
    ) as file:
        return file.read()