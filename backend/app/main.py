import hashlib
import uuid
from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from app.core.config import settings
from app.db import get_session, init_db
from app.models.vote import Vote, VoteCreate, VoteRead


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Initialize SQLModel tables
    init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for student identification, vote recording, and receipt generation using SQLModel and Turso/SQLite",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS configuration for Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["System"])
def health_check():
    """System health check endpoint verifying database mode."""
    is_turso = bool(settings.TURSO_DATABASE_URL and settings.TURSO_AUTH_TOKEN)
    return {
        "status": "ok",
        "app": settings.PROJECT_NAME,
        "round": 1,
        "database": "turso-libsql" if is_turso else "sqlite-fallback",
    }


@app.get(f"{settings.API_V1_PREFIX}/health", tags=["System"])
def api_health_check():
    return health_check()


@app.get(f"{settings.API_V1_PREFIX}/votes/check/{{student_id}}", tags=["Votes"])
def check_student_voted(student_id: str, session: Session = Depends(get_session)):
    """Verifies if a student has already voted in Round 1 (1 vote per student policy)."""
    statement = select(Vote).where(Vote.student_id == student_id.strip())
    existing = session.exec(statement).first()
    return {
        "student_id": student_id.strip(),
        "has_voted": existing is not None,
        "message": "El carné ya tiene un voto registrado"
        if existing
        else "Carné habilitado para votar",
    }


@app.post(
    f"{settings.API_V1_PREFIX}/votes",
    response_model=VoteRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Votes"],
)
def submit_vote(vote_in: VoteCreate, session: Session = Depends(get_session)):
    """
    Submits a student vote.
    Guarantees strict 1-vote-per-student idempotency/uniqueness.
    Generates verification receipt and cryptographic SHA-256 hash.
    """
    cleaned_id = vote_in.student_id.strip()

    # Duplicate check
    existing = session.exec(select(Vote).where(Vote.student_id == cleaned_id)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El estudiante con carné {cleaned_id} ya emitió su voto.",
        )

    # Generate receipt ID and timestamp
    now = datetime.now(UTC)
    receipt_id = f"ICD-VOTE-{now.strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"

    # Cryptographic proof
    raw_payload = (
        f"{receipt_id}:{cleaned_id}:{vote_in.figure_id}:{vote_in.palette_id}:{now.isoformat()}"
    )
    verification_hash = f"sha256:{hashlib.sha256(raw_payload.encode('utf-8')).hexdigest()}"

    vote = Vote(
        student_id=cleaned_id,
        student_name=vote_in.student_name.strip(),
        figure_id=vote_in.figure_id,
        palette_id=vote_in.palette_id,
        position_id=vote_in.position_id,
        rationale=vote_in.rationale,
        round=vote_in.round or 1,
        receipt_id=receipt_id,
        timestamp=now,
        verification_hash=verification_hash,
    )

    session.add(vote)
    session.commit()
    session.refresh(vote)
    return vote


@app.get(f"{settings.API_V1_PREFIX}/votes/stats", tags=["Votes"])
def get_voting_stats(session: Session = Depends(get_session)):
    """Returns aggregated voting statistics for Round 1."""
    votes = session.exec(select(Vote)).all()
    by_figure: dict[str, int] = {}
    for v in votes:
        by_figure[v.figure_id] = by_figure.get(v.figure_id, 0) + 1

    return {
        "total_votes": len(votes),
        "round": 1,
        "by_figure": by_figure,
    }
