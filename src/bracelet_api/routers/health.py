from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bracelet_api.database import get_db
from bracelet_api.models import Device, Health
from bracelet_api.schemas import HealthCreate, HealthOut

router = APIRouter(prefix="/health", tags=["health"])


@router.post("", response_model=HealthOut, status_code=201)
async def create_health_record(body: HealthCreate, db: AsyncSession = Depends(get_db)):
    device = await db.get(Device, body.device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    record = Health(
        device_id=body.device_id,
        sp0=body.sp0,
        heartbeat=body.heartbeat,
        is_moving=body.is_moving,
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


@router.get("", response_model=list[HealthOut])
async def get_latest_health_per_device(db: AsyncSession = Depends(get_db)):
    latest_ids = (
        select(Health.id)
        .distinct(Health.device_id)
        .order_by(Health.device_id, Health.created_at.desc())
        .subquery()
    )
    stmt = select(Health).where(Health.id.in_(select(latest_ids)))
    result = await db.execute(stmt)
    return list(result.scalars().all())
