from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base

if TYPE_CHECKING:
    from src.models.shipment import Shipment


class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    license_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relación Uno a Muchos con Shipments resolviendo por nombre de clase (String)
    shipments: Mapped[list["Shipment"]] = relationship("Shipment", back_populates="driver")


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    plate: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    capacity_kg: Mapped[float] = mapped_column(Float, nullable=False)

    # Relación Uno a Muchos con Shipments resolviendo por nombre de clase (String)
    shipments: Mapped[list["Shipment"]] = relationship("Shipment", back_populates="vehicle")