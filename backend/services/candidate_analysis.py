import os
import tempfile

from backend.services.document_parser import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_txt,
)

from backend.services.text_preprocessor import clean_text
from backend.services.text_analyzer import analyze_sentences
from backend.services.nltk_analyzer import analyze_with_nltk
from backend.services.tfidf_analyzer import analyze_with_tfidf
from backend.services.ml_detector import predict_ai_probability
from backend.services.perplexity_analyzer import calculate_perplexity
from backend.services.risk_scorer import calculate_ai_risk

from backend.services.metadata_analyzer import (
    extract_pdf_metadata,
    analyze_metadata,
)


def analyze_candidate_document(file_content: bytes, filename: str) -> dict:
    suffix = os.path.splitext(filename)[1].lower()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix,
    ) as temp:
        temp.write(file_content)
        temp_path = temp.name

    try:
        # -----------------------------------------------------
        # Document extraction
        # -----------------------------------------------------

        if suffix == ".pdf":

            text = extract_text_from_pdf(temp_path)

            metadata = extract_pdf_metadata(temp_path)

            metadata_analysis = analyze_metadata(metadata)

        elif suffix == ".docx":

            text = extract_text_from_docx(temp_path)

            metadata = {}

            metadata_analysis = {
                "suspicious_count": 0,
                "suspicious_fields": [],
            }

        elif suffix == ".txt":

            text = extract_text_from_txt(temp_path)

            metadata = {}

            metadata_analysis = {
                "suspicious_count": 0,
                "suspicious_fields": [],
            }

        else:
            raise ValueError("Unsupported document type")

        # -----------------------------------------------------
        # Text preprocessing
        # -----------------------------------------------------

        cleaned_text = clean_text(text)

        if not cleaned_text:
            raise ValueError(
                "No readable text found in the document"
            )

        # -----------------------------------------------------
        # Existing statistical NLP analysis
        # -----------------------------------------------------

        analysis = analyze_sentences(cleaned_text)

        # -----------------------------------------------------
        # NLTK analysis
        # -----------------------------------------------------

        nltk_analysis = analyze_with_nltk(
            cleaned_text
        )

        analysis.update(nltk_analysis)

        # -----------------------------------------------------
        # TF-IDF analysis
        # -----------------------------------------------------

        tfidf_analysis = analyze_with_tfidf(
            cleaned_text
        )

        analysis.update(tfidf_analysis)

        # -----------------------------------------------------
        # Trained ML classifier
        # -----------------------------------------------------

        ml_analysis = predict_ai_probability(
            cleaned_text
        )

        analysis.update(ml_analysis)

        # -----------------------------------------------------
        # Language-model perplexity
        #
        # Perplexity is currently recorded as an analysis
        # feature only. It is NOT yet added to the risk score.
        # -----------------------------------------------------

        perplexity_analysis = calculate_perplexity(
            cleaned_text
        )

        analysis.update(perplexity_analysis)

        # -----------------------------------------------------
        # Combined AI risk scoring
        # -----------------------------------------------------

        risk = calculate_ai_risk(
            analysis,
            metadata_analysis,
        )

        # -----------------------------------------------------
        # Final result
        # -----------------------------------------------------

        return {
            "filename": filename,
            "analysis": analysis,
            "metadata": metadata,
            "metadata_analysis": metadata_analysis,
            "risk": risk,
        }

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)