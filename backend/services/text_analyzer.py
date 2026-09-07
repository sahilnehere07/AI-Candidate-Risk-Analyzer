import re
import statistics
from collections import Counter


AI_BUZZWORDS = [
    "spearheaded cross-functional initiatives",
    "leveraged cutting-edge solutions",
    "testament to",
    "delve into",
]

AI_STYLE_PATTERNS = [
    r"\bdriving?\s+(?:meaningful\s+)?(?:digital\s+)?transformation\b",
    r"\bfoster(?:ing)?\s+(?:continuous\s+)?(?:collaborative\s+)?innovation\b",
    r"\bmaximize\s+(?:business\s+)?value\b",
    r"\b(?:demonstrated|proven)\s+(?:exceptional\s+)?(?:ability|expertise)\b",
    r"\bproven\s+track\s+record\b",
    r"\bleverag(?:e|ed|ing)\s+(?:innovative|emerging|cutting-edge)\s+(?:solutions|technologies)\b",
    r"\bseamless\s+(?:user\s+)?experiences\b",
    r"\bhigh-impact\s+solutions\b",
    r"\bimpactful\s+outcomes\b",
    r"\boperational\s+excellence\b",
]


def split_sentences(text: str) -> list[str]:
    raw_sentences = re.split(r"[.!?]+", text)

    sentences = []

    for sentence in raw_sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        words = sentence.split()

        if len(words) < 3:
            continue

        sentences.append(sentence)

    return sentences


def get_words(text: str) -> list[str]:
    return re.findall(r"\b[a-zA-Z]+\b", text.lower())


def calculate_ngram_density(text: str, n: int = 2) -> float:
    words = get_words(text)

    if len(words) < n:
        return 0.0

    ngrams = [
        tuple(words[i:i + n])
        for i in range(len(words) - n + 1)
    ]

    counts = Counter(ngrams)

    repeated_occurrences = sum(
        count
        for count in counts.values()
        if count > 1
    )

    total_ngrams = len(ngrams)

    return round(
        repeated_occurrences / total_ngrams,
        4,
    )


def calculate_vocabulary_diversity(text: str) -> float:
    words = get_words(text)

    if not words:
        return 0.0

    unique_words = len(set(words))

    return round(
        unique_words / len(words),
        4,
    )


def find_ai_style_patterns(text: str) -> list[str]:
    matches = []

    for pattern in AI_STYLE_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            matches.append(pattern)

    return matches


def analyze_sentences(text: str) -> dict:
    sentences = split_sentences(text)

    sentence_lengths = [
        len(sentence.split())
        for sentence in sentences
    ]

    average_length = (
        sum(sentence_lengths) / len(sentence_lengths)
        if sentence_lengths
        else 0
    )

    if len(sentence_lengths) > 1:
        burstiness = statistics.stdev(sentence_lengths)
    else:
        burstiness = 0

    text_lower = text.lower()

    flagged_phrases = [
        phrase
        for phrase in AI_BUZZWORDS
        if phrase in text_lower
    ]

    ai_style_patterns = find_ai_style_patterns(text)

    bigram_density = calculate_ngram_density(
        text,
        n=2,
    )

    trigram_density = calculate_ngram_density(
        text,
        n=3,
    )

    vocabulary_diversity = calculate_vocabulary_diversity(
        text
    )

    return {
        "sentence_count": len(sentences),
        "sentence_lengths": sentence_lengths,
        "average_sentence_length": round(
            average_length,
            2,
        ),
        "burstiness": round(
            burstiness,
            2,
        ),
        "buzzword_count": len(flagged_phrases),
        "flagged_phrases": flagged_phrases,
        "ai_style_pattern_count": len(ai_style_patterns),
        "ai_style_patterns": ai_style_patterns,
        "bigram_density": bigram_density,
        "trigram_density": trigram_density,
        "vocabulary_diversity": vocabulary_diversity,
    }