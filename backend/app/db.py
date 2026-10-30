import os
from collections.abc import Generator
from typing import Any, cast

import libsql
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings


class LibsqlConnectionProxy:
    """
    Transparent proxy around raw libsql.Connection to satisfy
    SQLAlchemy's pysqlite dialect expectations (e.g. create_function).
    """

    _raw: Any

    def __init__(self, raw_conn: Any) -> None:
        self._raw = raw_conn

    def create_function(self, *args: Any, **kwargs: Any) -> None:
        pass

    def __getattr__(self, name: str) -> Any:
        return getattr(self._raw, name)


def create_db_engine():
    """
    Creates an engine using SQLModel:
    - If TURSO_DATABASE_URL & TURSO_AUTH_TOKEN are provided, connects via Turso's official libSQL driver.
    - Otherwise, falls back to local SQLite with thread safety enabled.
    """
    turso_url = settings.TURSO_DATABASE_URL
    auth_token = settings.TURSO_AUTH_TOKEN

    if turso_url and turso_url.startswith(("libsql://", "https://")) and auth_token:
        # Turso Cloud via official libSQL client (with optional local replica syncing)
        def connect_turso() -> LibsqlConnectionProxy:
            raw_conn = cast(Any, libsql).connect(
                settings.LOCAL_DB_PATH,
                sync_url=turso_url,
                auth_token=auth_token,
            )
            return LibsqlConnectionProxy(raw_conn)

        return create_engine("sqlite://", creator=connect_turso)

    # Standard SQLite Fallback
    db_path = settings.LOCAL_DB_PATH
    os.makedirs(
        os.path.dirname(os.path.abspath(db_path)), exist_ok=True
    ) if "/" in db_path else None
    return create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )


engine = create_db_engine()


def init_db() -> None:
    """Initializes tables in database."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency for database sessions."""
    with Session(engine) as session:
        yield session
