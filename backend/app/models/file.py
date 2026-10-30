from datetime import UTC, datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.vote import Vote


class VoteFile(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    vote_id: int = Field(foreign_key="vote.id", index=True, description="ID del voto asociado")
    filename: str = Field(description="Nombre original del archivo subido")
    content_type: str = Field(description="MIME type del archivo (ej. application/pdf, image/png)")
    file_size: int = Field(description="Tamaño en bytes")
    data: bytes = Field(description="Contenido binario en formato BLOB")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Fecha y hora de subida (UTC)",
    )

    vote: Optional["Vote"] = Relationship(back_populates="file")


class VoteFileRead(SQLModel):
    id: int
    vote_id: int
    filename: str
    content_type: str
    file_size: int
    created_at: datetime
