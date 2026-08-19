from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

# ==========================================
# SCHEMAS DE AUTENTICACIÓN / USUARIOS
# ==========================================

class UserBase(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Nayib de la Cruz"})
    email: EmailStr = Field(..., json_schema_extra={"example": "nayib@logitrack.com"})
    phone: Optional[str] = Field(None, json_schema_extra={"example": "+52 921 123 4567"})

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, json_schema_extra={"example": "contrasenaSegura123"})

class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# Schemas auxiliares para Tokens JWT
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None


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