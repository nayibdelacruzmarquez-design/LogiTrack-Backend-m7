from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.config.database import get_db
from src.models import Driver
from src.schemas.fleet import DriverCreate, DriverResponse

router = APIRouter()


@router.post("/", response_model=DriverResponse, status_code=status.HTTP_201_CREATED)
async def create_driver(driver_in: DriverCreate, db: AsyncSession = Depends(get_db)):
    new_driver = Driver(
        full_name=driver_in.full_name,
        email=driver_in.email,
        license_number=driver_in.license_number,
        is_active=True
    )
    db.add(new_driver)
    await db.commit()
    await db.refresh(new_driver)
    return new_driver


@router.get("/", response_model=List[DriverResponse])
async def list_drivers(db: AsyncSession = Depends(get_db)):
    stmt = select(Driver)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{driver_id}", response_model=DriverResponse)
async def get_driver(driver_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Driver).where(Driver.id == driver_id)
    result = await db.execute(stmt)
    driver = result.scalar_one_or_none()
    if not driver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conductor no encontrado")
    return driver