from fastapi import APIRouter, HTTPException, status
from typing import List
from src.schemas.fleet import VehicleCreate, VehicleResponse

router = APIRouter()

vehicles_db = []
vehicle_id_counter = 1

@router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
async def create_vehicle(vehicle_in: VehicleCreate):
    global vehicle_id_counter
    vehicle_dict = vehicle_in.model_dump()
    vehicle_dict["id"] = vehicle_id_counter
    vehicle_dict["is_active"] = True
    vehicles_db.append(vehicle_dict)
    vehicle_id_counter += 1
    return vehicle_dict

@router.get("/", response_model=List[VehicleResponse])
async def list_vehicles():
    return vehicles_db

@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(vehicle_id: int):
    for vehicle in vehicles_db:
        if vehicle["id"] == vehicle_id:
            return vehicle
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehículo no encontrado")