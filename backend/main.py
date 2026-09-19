from fastapi import (
    Depends,
    FastAPI,
    File,
    HTTPException,
    Request,
    UploadFile,
)
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.bot_detector import detect_bot
from backend.database import get_db
from backend.rate_limiter import check_rate_limit
from backend.schemas import (
    ApplicationSubmission,
    ApplicationSubmissionResponse,
    CandidateAnalysisResponse,
    CandidateDetailResponse,
    CandidateListItem,
    CandidateRiskRequest,
    CandidateRiskResponse,
)
from backend.services.candidate_analysis import (
    analyze_candidate_document,
)
from backend.services.candidate_repository import (
    build_candidate_detail,
    create_candidate,
    get_all_candidates,
    get_candidate_by_id,
)
from backend.services.candidate_risk import (
    build_candidate_risk,
)

import os


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MAX_FILE_SIZE = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {".pdf", ".docx"}


@app.get("/")
def root():
    return {
        "message": (
            "AI Candidate Risk Analyzer "
            "backend is running"
        )
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post(
    "/upload",
    response_model=CandidateAnalysisResponse,
)
async def upload_document(
    file: UploadFile = File(...),
):
    suffix = os.path.splitext(
        file.filename
    )[1].lower()

    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Only PDF and DOCX files "
                "are supported"
            ),
        )

    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=(
                "File size exceeds the 5 MB limit"
            ),
        )

    if not file_content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty",
        )

    try:
        result = analyze_candidate_document(
            file_content=file_content,
            filename=file.filename,
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unable to process the "
                "uploaded document"
            ),
        )


@app.post(
    "/submit-application",
    response_model=ApplicationSubmissionResponse,
)
def submit_application(
    application: ApplicationSubmission,
    request: Request,
):
    ip_address = request.client.host

    bot_result = detect_bot(
        honeypot_value=application.honeypot_value,
        time_taken_seconds=(
            application.time_taken_seconds
        ),
        user_agent=application.user_agent,
    )

    rate_result = check_rate_limit(
        ip_address
    )

    reasons = bot_result["reasons"].copy()

    if rate_result["is_rate_limited"]:
        reasons.append(
            "Too many submissions from "
            "this IP address"
        )

    is_bot = (
        bot_result["is_bot"]
        or rate_result["is_rate_limited"]
    )

    return {
        "bot_detection": {
            "is_bot": is_bot,
            "reason_count": len(reasons),
            "reasons": reasons,
        },
        "rate_limit": rate_result,
    }


@app.post(
    "/candidate-risk",
    response_model=CandidateRiskResponse,
)
def candidate_risk(
    request_data: CandidateRiskRequest,
    db: Session = Depends(get_db),
):
    result = build_candidate_risk(
        ai_risk=request_data.ai_risk.model_dump(),
        bot_detection=(
            request_data.bot_detection.model_dump()
        ),
        rate_limit=(
            request_data.rate_limit.model_dump()
            if request_data.rate_limit
            else None
        ),
    )

    candidate = create_candidate(
        db=db,
        name=request_data.name,
        email=request_data.email,
        resume_filename=(
            request_data.resume_filename
        ),
        ai_risk=request_data.ai_risk.model_dump(),
        bot_detection=(
            request_data.bot_detection.model_dump()
        ),
        rate_limit=(
            request_data.rate_limit.model_dump()
            if request_data.rate_limit
            else None
        ),
        analysis=request_data.analysis.model_dump(),
        overall_status=result["overall_status"],
    )

    return {
        "candidate_id": candidate.id,
        **result,
    }


@app.get(
    "/candidates",
    response_model=list[CandidateListItem],
)
def get_candidates(
    db: Session = Depends(get_db),
):
    candidates = get_all_candidates(db)

    return candidates


@app.get(
    "/candidates/{candidate_id}",
    response_model=CandidateDetailResponse,
)
def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
):
    candidate = get_candidate_by_id(
        db,
        candidate_id,
    )

    if candidate is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found",
        )

    return build_candidate_detail(candidate)