from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.config.database import get_db
from src.models.shipment import Shipment
from src.schemas.shipment import ShipmentCreate, ShipmentResponse, ShipmentStatus

router = APIRouter()


@router.post(
    "/", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED
)
async def create_shipment(
    shipment_in: ShipmentCreate, db: AsyncSession = Depends(get_db)
):
  # Instanciar modelo ORM con los datos recibidos
  new_shipment = Shipment(
      tracking_number=shipment_in.tracking_number,
      weight=shipment_in.weight,
      status=ShipmentStatus.PENDING,
      client_id=shipment_in.client_id,
      origin_location_id=shipment_in.origin_location_id,
      destination_location_id=shipment_in.destination_location_id,
  )

  db.add(new_shipment)
  await db.commit()
  await db.refresh(new_shipment)
  return new_shipment


@router.get("/", response_model=List[ShipmentResponse])
async def list_shipments(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
  # Consulta optimizada para evitar el problema N+1 mediante selectinload
  stmt = (
      select(Shipment)
      .options(
          selectinload(Shipment.client),
          selectinload(Shipment.vehicle),
          selectinload(Shipment.driver),
      )
      .offset(skip)
      .limit(limit)
  )

  result = await db.execute(stmt)
  return result.scalars().all()


@router.get("/{shipment_id}", response_model=ShipmentResponse)
async def get_shipment(shipment_id: int, db: AsyncSession = Depends(get_db)):
  stmt = (
      select(Shipment)
      .options(
          selectinload(Shipment.client),
          selectinload(Shipment.vehicle),
          selectinload(Shipment.driver),
      )
      .where(Shipment.id == shipment_id)
  )

  result = await db.execute(stmt)
  shipment = result.scalar_one_or_none()

  if not shipment:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Envío no encontrado"
    )

  return shipment


@router.delete("/{shipment_id}", status_code=status.HTTP_200_OK)
async def delete_shipment(
    shipment_id: int, db: AsyncSession = Depends(get_db)
):
  stmt = select(Shipment).where(Shipment.id == shipment_id)
  result = await db.execute(stmt)
  shipment = result.scalar_one_or_none()

  if not shipment:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Envío no encontrado"
    )

  await db.delete(shipment)
  await db.commit()

  return {"message": f"Envío {shipment_id} eliminado exitosamente"}