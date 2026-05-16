from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bracelet_api.database import get_db
from bracelet_api.models import Device, GPS
from bracelet_api.schemas import GPSOut, GPSPosition

router = APIRouter(prefix="/gps", tags=["gps"])


@router.post("", response_model=GPSOut, status_code=201)
async def create_gps_record(body: GPSPosition, db: AsyncSession = Depends(get_db)):
    device = await db.get(Device, body.device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
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
    latest_ids = (
        select(GPS.id)
        .distinct(GPS.device_id)
        .order_by(GPS.device_id, GPS.created_at.desc())
        .subquery()
    )
    stmt = select(GPS).where(GPS.id.in_(select(latest_ids)))
    result = await db.execute(stmt)
    return list(result.scalars().all())
