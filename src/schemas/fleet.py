from pydantic import BaseModel, Field
from typing import Optional

class VehicleBase(BaseModel):
    plate_number: str = Field(..., example="ABC-1234")
    model: str = Field(..., example="Volvo FH16")
    capacity_tons: float = Field(..., gt=0, example=20.0)

class VehicleCreate(VehicleBase):
    pass

class VehicleResponse(VehicleBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True