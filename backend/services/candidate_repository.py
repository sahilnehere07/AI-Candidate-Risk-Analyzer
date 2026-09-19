import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models import Candidate


def create_candidate(
    db: Session,
    name: str,
    email: str,
    resume_filename: str,
    ai_risk: dict,
    bot_detection: dict,
    rate_limit: dict | None,
    analysis: dict,
    overall_status: str,
) -> Candidate:
    candidate = Candidate(
        name=name,
        email=email,
        resume_filename=resume_filename,
        ai_risk_score=ai_risk["ai_risk_score"],
        ai_classification=ai_risk["classification"],
        ai_signals=json.dumps(ai_risk.get("signals", [])),
        ai_contributions=json.dumps(
            ai_risk.get("contributions", [])
        ),
        bot_detected=bot_detection["is_bot"],
        bot_reasons=json.dumps(
            bot_detection.get("reasons", [])
        ),
        bot_reason_count=bot_detection.get(
            "reason_count",
            0,
        ),
        rate_limited=(
            rate_limit["is_rate_limited"]
            if rate_limit
            else False
        ),
        sentence_count=analysis.get(
            "sentence_count",
            0,
        ),
        average_sentence_length=analysis.get(
            "average_sentence_length",
            0,
        ),
        burstiness=analysis.get(
            "burstiness",
            0,
        ),
        bigram_density=analysis.get(
            "bigram_density",
            0,
        ),
        trigram_density=analysis.get(
            "trigram_density",
            0,
        ),
        vocabulary_diversity=analysis.get(
            "vocabulary_diversity",
            0,
        ),
        overall_status=overall_status,
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return candidate


def get_all_candidates(db: Session) -> list[Candidate]:
    statement = (
        select(Candidate)
        .order_by(Candidate.created_at.desc())
    )

    return list(db.scalars(statement).all())


def get_candidate_by_id(
    db: Session,
    candidate_id: int,
) -> Candidate | None:
    statement = select(Candidate).where(
        Candidate.id == candidate_id
    )

    return db.scalars(statement).first()


def build_candidate_detail(
    candidate: Candidate,
) -> dict:
    return {
        "id": candidate.id,
        "name": candidate.name,
        "email": candidate.email,
        "resume_filename": candidate.resume_filename,
        "ai_risk_score": candidate.ai_risk_score,
        "ai_classification": candidate.ai_classification,
        "ai_signals": json.loads(
            candidate.ai_signals or "[]"
        ),
        "ai_contributions": json.loads(
            candidate.ai_contributions or "[]"
        ),
        "bot_detected": candidate.bot_detected,
        "bot_reasons": json.loads(
            candidate.bot_reasons or "[]"
        ),
        "bot_reason_count": candidate.bot_reason_count,
        "rate_limited": candidate.rate_limited,
        "sentence_count": candidate.sentence_count,
        "average_sentence_length": (
            candidate.average_sentence_length
        ),
        "burstiness": candidate.burstiness,
        "bigram_density": candidate.bigram_density,
        "trigram_density": candidate.trigram_density,
        "vocabulary_diversity": (
            candidate.vocabulary_diversity
        ),
        "overall_status": candidate.overall_status,
        "created_at": candidate.created_at,
    }