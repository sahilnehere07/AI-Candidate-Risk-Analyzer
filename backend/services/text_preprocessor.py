import re


def clean_text(text: str) -> str:

    # Normalize line breaks
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove repeated blank lines
    text = re.sub(r"\n{2,}", "\n", text)

    # Clean each line
    lines = text.split("\n")

    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()