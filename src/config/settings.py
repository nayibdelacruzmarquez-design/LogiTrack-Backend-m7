import os


class Settings:
    PROJECT_NAME: str = "LogiTrack API"
    VERSION: str = "1.0.0"

    # Base de Datos
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./logitrack.db")

    # Celery & Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Seguridad JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-logitrack-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


settings = Settings()