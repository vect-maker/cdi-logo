import libsql
from app.core.config import settings


def get_db_connection() -> libsql.Connection:
    """
    Creates a libSQL connection.
    If TURSO_DATABASE_URL and TURSO_AUTH_TOKEN are provided, connects to Turso Cloud.
    Otherwise, uses the local database file for offline development.
    """
    if settings.TURSO_DATABASE_URL and settings.TURSO_AUTH_TOKEN:
        return libsql.connect(
            settings.LOCAL_DB_PATH,
            sync_url=settings.TURSO_DATABASE_URL,
            auth_token=settings.TURSO_AUTH_TOKEN,
        )
    return libsql.connect(settings.LOCAL_DB_PATH)
