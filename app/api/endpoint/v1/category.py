import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dto.core.category import GetListCategoryResponse
from app.helper.base_response import DataResponse
from app.helper.db import db_session
from app.service.category import CategoryService



router = APIRouter()

_logger = logging.getLogger(__name__)


@router.get('/list-category', response_model=DataResponse[GetListCategoryResponse])
def get_list_category(db: Session = Depends(db_session)):
    data = CategoryService.get_list_category(db)
    return DataResponse().success_response(data=data)
