from typing import TYPE_CHECKING
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base

if TYPE_CHECKING:
    from src.models.shipment import Shipment

# Tabla intermedia Muchos a Muchos: Clientes <-> Ubicaciones
client_locations = Table(
    "client_locations",
    Base.metadata,
    Column(
        "client_id",
        ForeignKey("clients.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "location_id",
        ForeignKey("locations.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(30), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Uno a Muchos con Shipments (Apuntando por String para evitar ciclo)
    shipments: Mapped[list["Shipment"]] = relationship("Shipment", back_populates="client")

    # Muchos a Muchos con Locations
    locations: Mapped[list["Location"]] = relationship(
        secondary=client_locations, back_populates="clients"
    )


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    address: Mapped[str] = mapped_column(String(200), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)

    clients: Mapped[list["Client"]] = relationship(
        secondary=client_locations, back_populates="locations"
    )