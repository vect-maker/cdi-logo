from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for student identification, vote recording, and receipt generation",
    version="0.1.0",
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
    """Simple root health check endpoint."""
    return {
        "status": "ok",
        "app": settings.PROJECT_NAME,
        "round": 1,
        "database": "turso-libsql",
    }


@app.get(f"{settings.API_V1_PREFIX}/health", tags=["System"])
def api_health_check():
    """Versioned API health check endpoint."""
    return health_check()
