from datetime import datetime

from pydantic import BaseModel


class HealthCreate(BaseModel):
    device_id: str
    sp0: float
    heartbeat: float


class HealthOut(BaseModel):
    device_id: str
    sp0: float
    heartbeat: float
    created_at: datetime

    model_config = {"from_attributes": True}


class GPSPosition(BaseModel):
    device_id: str
    latitude: float
    longitude: float


class GPSOut(BaseModel):
    device_id: str
    latitude: float
    longitude: float
    created_at: datetime

    model_config = {"from_attributes": True}


class DeviceCreate(BaseModel):
    pass


class DeviceOut(BaseModel):
    id: str

    model_config = {"from_attributes": True}
