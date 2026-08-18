from fastapi import APIRouter, HTTPException, status
from typing import List
from src.schemas.user import DriverCreate, DriverResponse

router = APIRouter()

drivers_db = []
driver_id_counter = 1

@router.post("/", response_model=DriverResponse, status_code=status.HTTP_201_CREATED)
async def create_driver(driver_in: DriverCreate):
    global driver_id_counter
    driver_dict = driver_in.model_dump()
    driver_dict["id"] = driver_id_counter
    driver_dict["is_active"] = True
    drivers_db.append(driver_dict)
    driver_id_counter += 1
    return driver_dict

@router.get("/", response_model=List[DriverResponse])
async def list_drivers():
    return drivers_db

@router.get("/{driver_id}", response_model=DriverResponse)
async def get_driver(driver_id: int):
    for driver in drivers_db:
        if driver["id"] == driver_id:
            return driver
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conductor no encontrado")