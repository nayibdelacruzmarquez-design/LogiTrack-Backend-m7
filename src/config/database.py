import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://logitrack_user:secure_password123@localhost:5432/logitrack_db",
)

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


# Importamos todos los modelos ORM explícitamente desde __init__.py
try:
    from src.models import Client, Driver, Location, Shipment, Vehicle  # noqa: F401
except ImportError as e:
    print(f"Advertencia importando modelos: {e}")


async def init_db():
    """Crea automáticamente todas las tablas en la base de datos mediante el ORM si no existen."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session