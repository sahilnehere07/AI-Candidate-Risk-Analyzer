import re

import nltk


def _fallback_tokenize(text: str) -> list[str]:
    """
    Lightweight tokenizer used when NLTK tokenizer data
    is unavailable in the deployment environment.
    """
    return re.findall(r"\b[a-zA-Z]+\b", text.lower())


def _fallback_sentences(text: str) -> list[str]:
    """
    Lightweight sentence splitter used when NLTK's
    punkt_tab resource is unavailable.
    """
    sentences = re.split(r"[.!?]+", text)

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def analyze_with_nltk(text: str) -> dict:
    """
    Perform basic NLP analysis using NLTK.

    If NLTK tokenizer resources are unavailable,
    automatically falls back to lightweight regex
    tokenization so production analysis continues
    without failure.
    """

    if not text or not text.strip():
        return {
            "nltk_sentence_count": 0,
            "nltk_word_count": 0,
            "nltk_average_word_length": 0.0,
            "nltk_unique_word_ratio": 0.0,
            "nltk_long_word_ratio": 0.0,
        }

    try:
        # Try the normal NLTK tokenizers first.
        sentences = nltk.sent_tokenize(text)
        words = nltk.word_tokenize(text)

        words = [
            word.lower()
            for word in words
            if re.search(r"[A-Za-z]", word)
        ]

    except LookupError:
        # Render may not have NLTK's punkt_tab resource.
        # Use the safe local fallback instead.
        sentences = _fallback_sentences(text)
        words = _fallback_tokenize(text)

    if not words:
        return {
            "nltk_sentence_count": len(sentences),
            "nltk_word_count": 0,
            "nltk_average_word_length": 0.0,
            "nltk_unique_word_ratio": 0.0,
            "nltk_long_word_ratio": 0.0,
        }

    word_lengths = [
        len(word)
        for word in words
    ]

    average_word_length = (
        sum(word_lengths) / len(word_lengths)
    )

    unique_word_ratio = (
        len(set(words)) / len(words)
    )

    long_word_ratio = (
        sum(
            1
            for word in words
            if len(word) >= 7
        )
        / len(words)
    )

    return {
        "nltk_sentence_count": len(sentences),
        "nltk_word_count": len(words),
        "nltk_average_word_length": round(
            average_word_length,
            2,
        ),
        "nltk_unique_word_ratio": round(
            unique_word_ratio,
            4,
        ),
        "nltk_long_word_ratio": round(
            long_word_ratio,
            4,
        ),
    }