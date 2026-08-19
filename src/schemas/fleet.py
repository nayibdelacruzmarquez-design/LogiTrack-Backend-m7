from pydantic import BaseModel, EmailStr, Field


# ==========================================
# SCHEMAS DE VEHÍCULOS
# ==========================================

class VehicleBase(BaseModel):
    plate: str = Field(..., example="ABC-1234")
    model: str = Field(..., example="Volvo FH16")
    capacity_kg: float = Field(..., gt=0, example=20000.0)


class VehicleCreate(VehicleBase):
    pass


class VehicleResponse(VehicleBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True


# ==========================================
# SCHEMAS DE CONDUCTORES (DRIVERS)
# ==========================================

class DriverBase(BaseModel):
    full_name: str = Field(..., example="Carlos Mendoza")
    email: EmailStr = Field(..., example="carlos.mendoza@logitrack.com")
    license_number: str = Field(..., example="LIC-98765432")


class DriverCreate(DriverBase):
    pass


class DriverResponse(DriverBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True