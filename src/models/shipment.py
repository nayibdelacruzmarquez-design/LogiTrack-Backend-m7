from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base

if TYPE_CHECKING:
    from src.models.fleet import Driver, Vehicle
    from src.models.user import Client  # Se habilita la referencia para type checking


class Shipment(Base):
    __tablename__ = "shipments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tracking_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="PENDING")

    # Campos de direcciones y peso
    origin_address: Mapped[str] = mapped_column(String(255), nullable=False)
    destination_address: Mapped[str] = mapped_column(String(255), nullable=False)
    weight_kg: Mapped[float] = mapped_column(Float, nullable=False)

    # Claves Foráneas (Relaciones explícitas con ON DELETE SET NULL)
    client_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("clients.id", ondelete="SET NULL"), nullable=True
    )
    driver_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("drivers.id", ondelete="SET NULL"), nullable=True
    )
    vehicle_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("vehicles.id", ondelete="SET NULL"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relaciones ORM utilizando Strings para evitar ciclos en runtime
    client: Mapped[Optional["Client"]] = relationship("Client", back_populates="shipments")
    driver: Mapped[Optional["Driver"]] = relationship("Driver", back_populates="shipments")
    vehicle: Mapped[Optional["Vehicle"]] = relationship("Vehicle", back_populates="shipments")