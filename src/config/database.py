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


# Registramos los modelos ORM en Base para que create_all sepa qué tablas construir
try:
    from src.models.user import Client  # noqa: F401
    # Si tienes más modelos en src/models, impórtalos aquí:
    # from src.models.shipment import Shipment # noqa: F401
    # from src.models.vehicle import Vehicle # noqa: F401
    # from src.models.driver import Driver # noqa: F401
except ImportError:
    pass


async def init_db():
    """Crea automáticamente todas las tablas en la base de datos si no existen."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session