from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.auth.dependencies import get_current_user  # 🔒 Autenticación JWT
from src.config.database import get_db
from src.models.shipment import Shipment
from src.schemas.shipment import ShipmentCreate, ShipmentResponse

router = APIRouter(tags=["Envíos"])


@router.post("/", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
async def create_shipment(
    shipment_in: ShipmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)  # 🔒 Activa el candado en POST
):
    existing_shipment = await db.execute(
        select(Shipment).where(Shipment.tracking_number == shipment_in.tracking_number)
    )
    if existing_shipment.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El número de rastreo '{shipment_in.tracking_number}' ya se encuentra registrado."
        )

    db_shipment = Shipment(**shipment_in.model_dump())
    db.add(db_shipment)

    await db.commit()
    await db.refresh(db_shipment)
    return db_shipment


@router.get("/", response_model=List[ShipmentResponse])
async def get_shipments(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)  # 🔒 Activa el candado en GET
):
    stmt = (
        select(Shipment)
        .options(
            selectinload(Shipment.driver),
            selectinload(Shipment.vehicle),
            selectinload(Shipment.client)
        )
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()