from datetime import datetime

from pydantic import BaseModel


class ApplicationSubmission(BaseModel):
    honeypot_value: str = ""
    time_taken_seconds: float
    user_agent: str = ""


class AnalysisResult(BaseModel):
    sentence_count: int
    sentence_lengths: list[int]
    average_sentence_length: float
    burstiness: float
    buzzword_count: int
    flagged_phrases: list[str]
    ai_style_pattern_count: int
    ai_style_patterns: list[str]
    bigram_density: float
    trigram_density: float
    vocabulary_diversity: float


class MetadataResult(BaseModel):
    author: str | None = None
    creator: str | None = None
    producer: str | None = None
    creation_date: str | None = None
    modification_date: str | None = None


class SuspiciousMetadataField(BaseModel):
    field: str
    value: str
    reason: str


class MetadataAnalysisResult(BaseModel):
    suspicious_count: int
    suspicious_fields: list[SuspiciousMetadataField]


class RiskContribution(BaseModel):
    signal: str
    points: int


class RiskResult(BaseModel):
    ai_risk_score: int
    classification: str
    signals: list[str]
    contributions: list[RiskContribution]


class CandidateAnalysisResponse(BaseModel):
    filename: str
    analysis: AnalysisResult
    metadata: MetadataResult
    metadata_analysis: MetadataAnalysisResult
    risk: RiskResult


class BotDetectionResult(BaseModel):
    is_bot: bool
    reason_count: int
    reasons: list[str]


class RateLimitResult(BaseModel):
    ip_address: str
    submission_count: int
    is_rate_limited: bool
    limit: int
    window_seconds: int


class ApplicationSubmissionResponse(BaseModel):
    bot_detection: BotDetectionResult
    rate_limit: RateLimitResult


class CandidateRiskRequest(BaseModel):
    name: str
    email: str
    resume_filename: str
    analysis: AnalysisResult
    ai_risk: RiskResult
    bot_detection: BotDetectionResult
    rate_limit: RateLimitResult | None = None


class CandidateRiskAIContent(BaseModel):
    score: int
    classification: str
    signals: list[str]
    contributions: list[RiskContribution]


class CandidateRiskBotBehavior(BaseModel):
    is_bot: bool
    reason_count: int
    reasons: list[str]
    rate_limited: bool | None = None


class CandidateRiskResponse(BaseModel):
    candidate_id: int
    overall_status: str
    ai_content: CandidateRiskAIContent
    bot_behavior: CandidateRiskBotBehavior


class CandidateListItem(BaseModel):
    id: int
    name: str
    email: str
    resume_filename: str
    ai_risk_score: int
    ai_classification: str
    bot_detected: bool
    overall_status: str
    created_at: datetime


class CandidateDetailResponse(BaseModel):
    id: int
    name: str
    email: str
    resume_filename: str

    ai_risk_score: int
    ai_classification: str
    ai_signals: list[str]
    ai_contributions: list[RiskContribution]

    bot_detected: bool
    bot_reasons: list[str]
    bot_reason_count: int
    rate_limited: bool

    sentence_count: int
    average_sentence_length: float
    burstiness: float
    bigram_density: float
    trigram_density: float
    vocabulary_diversity: float

    overall_status: str
    created_at: datetime