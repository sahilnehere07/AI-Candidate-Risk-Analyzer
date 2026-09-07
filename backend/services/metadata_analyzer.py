import pdfplumber


SUSPICIOUS_METADATA_TOOLS = [
    "pdfkit",
    "puppeteer",
    "chatgpt",
]


def extract_pdf_metadata(file_path: str) -> dict:
    """
    Extract common PDF metadata fields.

    Missing metadata is normal, so missing values are returned as None.
    """

    with pdfplumber.open(file_path) as pdf:
        metadata = pdf.metadata or {}

    return {
        "author": metadata.get("Author"),
        "creator": metadata.get("Creator"),
        "producer": metadata.get("Producer"),
        "creation_date": metadata.get("CreationDate"),
        "modification_date": metadata.get("ModDate"),
    }


def analyze_metadata(metadata: dict) -> dict:
    """
    Identify metadata fields containing known tool names.

    Metadata is treated only as a supporting signal.
    It does not prove that a document was AI-generated.
    """

    suspicious_fields = []

    for field in ["author", "creator", "producer"]:
        value = metadata.get(field)

        if not value:
            continue

        value_lower = str(value).lower()

        for tool in SUSPICIOUS_METADATA_TOOLS:
            if tool in value_lower:
                suspicious_fields.append(
                    {
                        "field": field,
                        "value": value,
                        "reason": (
                            f"Contains suspicious tool name: {tool}"
                        ),
                    }
                )

    return {
        "suspicious_count": len(suspicious_fields),
        "suspicious_fields": suspicious_fields,
    }