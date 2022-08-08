from fastapi import APIRouter
from . import health, file_elastic, file, category, auth

v1_router = APIRouter()

v1_router.include_router(health.router, prefix="/health", tags=['health-check'])
v1_router.include_router(file_elastic.router, prefix="/elastic-file", tags=['ElasticFile'])
v1_router.include_router(file.router, prefix="/file", tags=['File'])
v1_router.include_router(category.router, prefix="/category", tags=['Category'])
v1_router.include_router(auth.router, prefix='/auth', tags=['auth'])
