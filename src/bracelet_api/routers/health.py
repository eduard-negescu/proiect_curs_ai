from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bracelet_api.database import get_db
from bracelet_api.models import Health
from bracelet_api.schemas import HealthCreate, HealthOut

router = APIRouter(prefix="/health", tags=["health"])


@router.post("", response_model=HealthOut, status_code=201)
async def create_health_record(body: HealthCreate, db: AsyncSession = Depends(get_db)):
    record = Health(
        device_id=body.device_id, sp0=body.sp0, heartbeat=body.heartbeat
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


@router.get("", response_model=list[HealthOut])
async def get_latest_health_per_device(db: AsyncSession = Depends(get_db)):
    subq = (
        select(
            Health.device_id,
            Health.id,
            Health.sp0,
            Health.heartbeat,
            Health.created_at,
        )
        .distinct(Health.device_id)
        .order_by(Health.device_id, Health.created_at.desc())
        .subquery()
    )
    result = await db.execute(select(subq))
    return list(result.scalars().all())
