from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bracelet_api.database import get_db
from bracelet_api.models import Device
from bracelet_api.schemas import DeviceOut

router = APIRouter(prefix="/device", tags=["device"])


@router.post("", response_model=DeviceOut, status_code=201)
async def create_device(db: AsyncSession = Depends(get_db)):
    device = Device()
    db.add(device)
    await db.commit()
    await db.refresh(device)
    return device


@router.get("", response_model=list[DeviceOut])
async def get_all_devices(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device.id))
    device_ids = result.scalars().all()
    return [DeviceOut(id=d) for d in device_ids]
