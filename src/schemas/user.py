from pydantic import BaseModel, Field

class DriverBase(BaseModel):
    full_name: str = Field(..., example="Carlos Mendoza")
    email: str = Field(..., example="carlos.mendoza@logitrack.com")
    license_number: str = Field(..., example="LIC-98765432")

class DriverCreate(DriverBase):
    pass

class DriverResponse(DriverBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True