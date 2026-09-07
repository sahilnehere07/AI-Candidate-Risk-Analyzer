from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(320),
        nullable=False,
    )

    resume_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    ai_risk_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    ai_classification: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    ai_signals: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="[]",
    )

    ai_contributions: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="[]",
    )

    bot_detected: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    bot_reasons: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="[]",
    )

    bot_reason_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    rate_limited: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    sentence_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    average_sentence_length: Mapped[float] = mapped_column(
        nullable=False,
        default=0,
    )

    burstiness: Mapped[float] = mapped_column(
        nullable=False,
        default=0,
    )

    bigram_density: Mapped[float] = mapped_column(
        nullable=False,
        default=0,
    )

    trigram_density: Mapped[float] = mapped_column(
        nullable=False,
        default=0,
    )

    vocabulary_diversity: Mapped[float] = mapped_column(
        nullable=False,
        default=0,
    )

    overall_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )