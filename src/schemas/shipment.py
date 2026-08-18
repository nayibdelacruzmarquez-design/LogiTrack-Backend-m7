from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class ShipmentStatus(str, Enum):
    PENDING = "PENDING"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class ShipmentBase(BaseModel):
    tracking_number: str = Field(..., example="TRK-1002")
    origin_address: str = Field(..., example="Av. Insurgentes Sur 1602, CDMX")
    destination_address: str = Field(..., example="Av. Constitución 400, Monterrey")
    weight_kg: float = Field(..., gt=0, example=150.5)

class ShipmentCreate(ShipmentBase):
    driver_id: Optional[int] = None
    vehicle_id: Optional[int] = None

class ShipmentResponse(ShipmentBase):
    id: int
    status: ShipmentStatus
    driver_id: Optional[int] = None
    vehicle_id: Optional[int] = None

    class Config:
        from_attributes = True