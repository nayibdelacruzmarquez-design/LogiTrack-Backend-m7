from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.config.database import Base


class Driver(Base):
  __tablename__ = "drivers"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  full_name: Mapped[str] = mapped_column(String(100), nullable=False)
  email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
  license_number: Mapped[str] = mapped_column(
      String(50), unique=True, nullable=False
  )
  is_active: Mapped[bool] = mapped_column(Boolean, default=True)

  shipments: Mapped[list["Shipment"]] = relationship(back_populates="driver")


class Vehicle(Base):
  __tablename__ = "vehicles"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  plate: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
  model: Mapped[str] = mapped_column(String(50), nullable=False)
  capacity_kg: Mapped[float] = mapped_column(nullable=False)

  shipments: Mapped[list["Shipment"]] = relationship(back_populates="vehicle")