from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.config.database import Base


class Shipment(Base):
  __tablename__ = "shipments"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  tracking_number: Mapped[str] = mapped_column(
      String(50), unique=True, index=True
  )
  status: Mapped[str] = mapped_column(String(30), default="PENDING")
  weight: Mapped[float] = mapped_column(Float, nullable=False)

  # Claves Foráneas
  client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
  origin_location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
  destination_location_id: Mapped[int] = mapped_column(
      ForeignKey("locations.id")
  )
  vehicle_id: Mapped[int | None] = mapped_column(
      ForeignKey("vehicles.id"), nullable=True
  )
  driver_id: Mapped[int | None] = mapped_column(
      ForeignKey("drivers.id"), nullable=True
  )

  # Relaciones ORM
  client: Mapped["Client"] = relationship(back_populates="shipments")
  vehicle: Mapped["Vehicle"] = relationship(back_populates="shipments")
  driver: Mapped["Driver"] = relationship(back_populates="shipments")