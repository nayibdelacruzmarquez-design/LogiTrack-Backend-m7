from sqlalchemy import Boolean, Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.config.database import Base

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

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  name: Mapped[str] = mapped_column(String(100), nullable=False)
  email: Mapped[str] = mapped_column(
      String(100), unique=True, index=True, nullable=False
  )

  # Uno a Muchos con Shipments
  shipments: Mapped[list["Shipment"]] = relationship(back_populates="client")
  # Muchos a Muchos con Locations
  locations: Mapped[list["Location"]] = relationship(
      secondary=client_locations, back_populates="clients"
  )


class Location(Base):
  __tablename__ = "locations"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  address: Mapped[str] = mapped_column(String(200), nullable=False)
  city: Mapped[str] = mapped_column(String(100), nullable=False)

  clients: Mapped[list["Client"]] = relationship(
      secondary=client_locations, back_populates="locations"
  )