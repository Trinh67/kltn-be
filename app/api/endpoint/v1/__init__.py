from fastapi import APIRouter
from . import file_elastic, file, health

v1_router = APIRouter()

v1_router.include_router(health.router, prefix="/health", tags=['health-check'])
v1_router.include_router(file_elastic.router, prefix="/elastic-file", tags=['ElasticFile'])
v1_router.include_router(file.router, prefix="/file", tags=['File'])
