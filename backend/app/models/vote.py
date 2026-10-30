from datetime import UTC, datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.file import VoteFile


class VoteBase(SQLModel):
    student_id: str = Field(
        index=True, unique=True, description="Carné estudiantil de 8 dígitos numéricos"
    )
    student_name: str = Field(description="Nombre completo del estudiante")
    figure_id: str = Field(description="Identificador del isotipo seleccionado")
    palette_id: str = Field(description="Paleta cromática seleccionada")
    position_id: str = Field(description="Posición del logotipo en la prenda")
    rationale: str | None = Field(default=None, description="Justificación o retroalimentación")
    round: int = Field(default=1, description="Número de ronda del proceso iterativo")


class Vote(VoteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    receipt_id: str = Field(index=True, unique=True, description="Identificador único del recibo")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Fecha y hora de emisión (UTC con timezone)",
    )
    verification_hash: str = Field(
        description="Hash criptográfico SHA256 para verificación del voto"
    )

    file: Optional["VoteFile"] = Relationship(back_populates="vote")


class VoteCreate(VoteBase):
    pass


class VoteRead(VoteBase):
    id: int
    receipt_id: str
    timestamp: datetime
    verification_hash: str
    has_attachment: bool = False
    attachment_filename: str | None = None
