from fastapi import APIRouter
from . import health

v1_router = APIRouter()

v1_router.include_router(health.router, prefix="/health", tags=['health-check'])
