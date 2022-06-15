from fastapi import APIRouter
from . import health, file

v1_router = APIRouter()

v1_router.include_router(health.router, prefix="/health", tags=['health-check'])
v1_router.include_router(file.router, prefix="/file", tags=['File'])
