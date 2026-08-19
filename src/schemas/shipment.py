from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

# ==========================================
# SCHEMAS DE ENVÍOS (SHIPMENTS)
# ==========================================

class ShipmentBase(BaseModel):
    tracking_number: str = Field(..., json_schema_extra={"example": "TRK-1002"})
    origin_address: str = Field(..., json_schema_extra={"example": "Av. Insurgentes Sur 1602, CDMX"})
    destination_address: str = Field(..., json_schema_extra={"example": "Av. Constitución 400, Monterrey"})
    weight_kg: float = Field(..., gt=0, json_schema_extra={"example": 150.5})

class ShipmentCreate(ShipmentBase):
    pass

class ShipmentResponse(ShipmentBase):
    id: int
    status: str
    driver_id: Optional[int] = None
    vehicle_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)