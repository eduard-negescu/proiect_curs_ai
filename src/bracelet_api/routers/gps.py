from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bracelet_api.database import get_db
from bracelet_api.models import GPS
from bracelet_api.schemas import GPSOut, GPSPosition

router = APIRouter(prefix="/gps", tags=["gps"])


@router.post("", response_model=GPSOut, status_code=201)
async def create_gps_record(body: GPSPosition, db: AsyncSession = Depends(get_db)):
    record = GPS(
        device_id=body.device_id,
        latitude=body.latitude,
        longitude=body.longitude,
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


@router.get("", response_model=list[GPSOut])
async def get_latest_gps_per_device(db: AsyncSession = Depends(get_db)):
    subq = (
        select(
            GPS.device_id,
            GPS.id,
            GPS.latitude,
            GPS.longitude,
            GPS.created_at,
        )
        .distinct(GPS.device_id)
        .order_by(GPS.device_id, GPS.created_at.desc())
        .subquery()
    )
    result = await db.execute(select(subq))
    return list(result.scalars().all())
