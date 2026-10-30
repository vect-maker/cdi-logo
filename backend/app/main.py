import hashlib
import uuid
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Annotated

from fastapi import (
    Depends,
    FastAPI,
    File,
    Form,
    HTTPException,
    Request,
    Response,
    UploadFile,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from app.core.config import settings
from app.db import get_session, init_db
from app.models.file import VoteFile
from app.models.vote import Vote, VoteCreate, VoteRead

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/webp",
}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Initialize SQLModel tables (Vote and VoteFile)
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


def _process_vote_submission(
    cleaned_id: str,
    student_name: str,
    figure_id: str,
    palette_id: str,
    position_id: str,
    rationale: str | None,
    round_num: int,
    file_bytes: bytes | None,
    filename: str | None,
    content_type: str | None,
    session: Session,
) -> VoteRead:
    # 1. Duplicate check
    existing = session.exec(select(Vote).where(Vote.student_id == cleaned_id)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El estudiante con carné {cleaned_id} ya emitió su voto.",
        )

    # 2. Generate receipt ID and timestamp
    now = datetime.now(UTC)
    receipt_id = f"ICD-VOTE-{now.strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"

    # 3. Cryptographic proof
    raw_payload = f"{receipt_id}:{cleaned_id}:{figure_id}:{palette_id}:{now.isoformat()}"
    verification_hash = f"sha256:{hashlib.sha256(raw_payload.encode('utf-8')).hexdigest()}"

    vote = Vote(
        student_id=cleaned_id,
        student_name=student_name.strip(),
        figure_id=figure_id,
        palette_id=palette_id,
        position_id=position_id,
        rationale=rationale,
        round=round_num or 1,
        receipt_id=receipt_id,
        timestamp=now,
        verification_hash=verification_hash,
    )
    session.add(vote)
    session.flush()  # assign vote.id

    assert vote.id is not None
    vote_file_record: VoteFile | None = None
    if file_bytes and filename and content_type:
        vote_file_record = VoteFile(
            vote_id=vote.id,
            filename=filename,
            content_type=content_type,
            file_size=len(file_bytes),
            data=file_bytes,
            created_at=now,
        )
        session.add(vote_file_record)

    session.commit()
    session.refresh(vote)

    return VoteRead(
        id=vote.id,
        student_id=vote.student_id,
        student_name=vote.student_name,
        figure_id=vote.figure_id,
        palette_id=vote.palette_id,
        position_id=vote.position_id,
        rationale=vote.rationale,
        round=vote.round,
        receipt_id=vote.receipt_id,
        timestamp=vote.timestamp,
        verification_hash=vote.verification_hash,
        has_attachment=vote_file_record is not None,
        attachment_filename=vote_file_record.filename if vote_file_record else None,
    )


@app.post(
    f"{settings.API_V1_PREFIX}/votes",
    response_model=VoteRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Votes"],
)
async def submit_vote(
    request: Request,
    session: Session = Depends(get_session),
    # Optional JSON body fields if Content-Type is application/json
    vote_in: VoteCreate | None = None,
    # Optional Multipart form fields
    student_id: Annotated[str | None, Form()] = None,
    student_name: Annotated[str | None, Form()] = None,
    figure_id: Annotated[str | None, Form()] = None,
    palette_id: Annotated[str | None, Form()] = None,
    position_id: Annotated[str | None, Form()] = None,
    rationale: Annotated[str | None, Form()] = None,
    round_num: Annotated[int | None, Form(alias="round")] = 1,
    file: Annotated[UploadFile | None, File()] = None,
):
    """
    Submits a student vote.
    Supports both multipart/form-data (with optional binary file upload)
    and legacy JSON payloads.
    Guarantees strict 1-vote-per-student uniqueness.
    """
    content_type = request.headers.get("content-type", "")

    file_bytes: bytes | None = None
    filename: str | None = None
    mime_type: str | None = None

    if "multipart/form-data" in content_type:
        if not student_id or not student_name or not figure_id or not palette_id or not position_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Faltan campos obligatorios en el formulario.",
            )

        if file and file.filename:
            # Validate MIME type
            if file.content_type not in ALLOWED_MIME_TYPES:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Tipo de archivo no permitido ({file.content_type}). Solo se admiten PDF e imágenes (PNG, JPG, WEBP).",
                )
            content = await file.read()
            if len(content) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El archivo excede el tamaño máximo permitido de 5 MB.",
                )
            file_bytes = content
            filename = file.filename
            mime_type = file.content_type

        return _process_vote_submission(
            cleaned_id=student_id.strip(),
            student_name=student_name,
            figure_id=figure_id,
            palette_id=palette_id,
            position_id=position_id,
            rationale=rationale,
            round_num=round_num or 1,
            file_bytes=file_bytes,
            filename=filename,
            content_type=mime_type,
            session=session,
        )

    # Legacy JSON body
    if vote_in is not None:
        return _process_vote_submission(
            cleaned_id=vote_in.student_id.strip(),
            student_name=vote_in.student_name,
            figure_id=vote_in.figure_id,
            palette_id=vote_in.palette_id,
            position_id=vote_in.position_id,
            rationale=vote_in.rationale,
            round_num=vote_in.round or 1,
            file_bytes=None,
            filename=None,
            content_type=None,
            session=session,
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Solicitud inválida: envíe JSON o multipart/form-data.",
    )


@app.get(f"{settings.API_V1_PREFIX}/votes/{{receipt_id}}/file", tags=["Votes"])
def download_vote_file(receipt_id: str, session: Session = Depends(get_session)):
    """Streams the binary file suggestion associated with a vote receipt."""
    vote = session.exec(select(Vote).where(Vote.receipt_id == receipt_id.strip())).first()
    if not vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voto no encontrado.",
        )

    assert vote.id is not None
    vote_file = session.exec(select(VoteFile).where(VoteFile.vote_id == vote.id)).first()
    if not vote_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El voto no tiene ningún archivo adjunto.",
        )

    return Response(
        content=vote_file.data,
        media_type=vote_file.content_type,
        headers={
            "Content-Disposition": f'inline; filename="{vote_file.filename}"',
            "Content-Length": str(vote_file.file_size),
        },
    )


@app.get(f"{settings.API_V1_PREFIX}/votes/stats", tags=["Votes"])
def get_voting_stats(session: Session = Depends(get_session)):
    """Returns aggregated voting statistics for Round 1."""
    votes = session.exec(select(Vote)).all()
    by_figure: dict[str, int] = {}
    with_attachments = 0

    for v in votes:
        by_figure[v.figure_id] = by_figure.get(v.figure_id, 0) + 1
        if session.exec(select(VoteFile).where(VoteFile.vote_id == v.id)).first():
            with_attachments += 1

    return {
        "total_votes": len(votes),
        "round": 1,
        "by_figure": by_figure,
        "with_attachments": with_attachments,
    }
