from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

# ==========================================
# SCHEMAS DE VEHÍCULOS (VEHICLES)
# ==========================================

class VehicleBase(BaseModel):
    plate: str = Field(..., json_schema_extra={"example": "ABC-1234"})
    model: str = Field(..., json_schema_extra={"example": "Volvo FH16"})
    capacity_kg: float = Field(..., gt=0, json_schema_extra={"example": 20000.0})

class VehicleCreate(VehicleBase):
    pass

class VehicleResponse(VehicleBase):
    id: int
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# SCHEMAS DE CONDUCTORES (DRIVERS)
# ==========================================

class DriverBase(BaseModel):
    full_name: str = Field(..., json_schema_extra={"example": "Carlos Mendoza"})
    email: EmailStr = Field(..., json_schema_extra={"example": "carlos.mendoza@logitrack.com"})
    license_number: str = Field(..., json_schema_extra={"example": "LIC-98765432"})

class DriverCreate(DriverBase):
    pass

class DriverResponse(DriverBase):
    id: int
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)