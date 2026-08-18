from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
async def login():
    """
    Endpoint temporal de autenticación (Se implementará formalmente en el módulo de seguridad).
    """
    return {"message": "Endpoint de autenticación listo para implementar JWT"}