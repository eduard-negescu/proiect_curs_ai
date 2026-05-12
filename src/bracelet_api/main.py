from contextlib import asynccontextmanager

from fastapi import FastAPI

from bracelet_api.routers import device, gps, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(health.router)
app.include_router(gps.router)
app.include_router(device.router)
