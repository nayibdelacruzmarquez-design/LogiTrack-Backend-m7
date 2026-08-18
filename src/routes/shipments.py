from fastapi import APIRouter, HTTPException, status
from typing import List
from src.schemas.shipment import ShipmentCreate, ShipmentResponse, ShipmentStatus

router = APIRouter()

shipments_db = []
shipment_id_counter = 1

@router.post("/", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
async def create_shipment(shipment_in: ShipmentCreate):
    global shipment_id_counter
    shipment_dict = shipment_in.model_dump()
    shipment_dict["id"] = shipment_id_counter
    shipment_dict["status"] = ShipmentStatus.PENDING
    shipments_db.append(shipment_dict)
    shipment_id_counter += 1
    return shipment_dict

@router.get("/", response_model=List[ShipmentResponse])
async def list_shipments(skip: int = 0, limit: int = 100):
    return shipments_db[skip : skip + limit]

@router.get("/{shipment_id}", response_model=ShipmentResponse)
async def get_shipment(shipment_id: int):
    for shipment in shipments_db:
        if shipment["id"] == shipment_id:
            return shipment
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Envío no encontrado")

@router.delete("/{shipment_id}", status_code=status.HTTP_200_OK)
async def delete_shipment(shipment_id: int):
    global shipments_db
    for index, shipment in enumerate(shipments_db):
        if shipment["id"] == shipment_id:
            shipments_db.pop(index)
            return {"message": f"Envío {shipment_id} eliminado exitosamente"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Envío no encontrado")