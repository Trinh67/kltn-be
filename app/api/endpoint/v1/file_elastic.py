import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dto.base import OpenApiResponseModel
from app.dto.core.auth import UserDTO
from app.dto.core.file import SearchFileMappingResponse
from app.helper.base_response import DataResponse, PagingDataResponse
from app.helper.db import db_session
from app.helper.middleware import get_current_user
from app.service.file_elastic import FileElasticService
from app.util.openapi import map_resp_to_openapi

from app.dto.core.file_elastic import CreateFileRequest, CreateFileResponse, GetFileResponse, GetListFileResponse, SearchFileRequest


router = APIRouter()

_logger = logging.getLogger(__name__)


@router.post("/", response_model=DataResponse[CreateFileResponse],
             response_description="Success",
             responses=map_resp_to_openapi([
                 OpenApiResponseModel(code=402, message='Param {param} is required', http_code='400',
                                      description='Missing required param'),
                 OpenApiResponseModel(code=417, message='{param} format is invalid', http_code='400',
                                      description='File path format is invalid'),
             ]))
def create_file(db: Session = Depends(db_session),
                                  *,
                                  request_input: CreateFileRequest, user: UserDTO = Depends(get_current_user)):
    data = FileElasticService.create_file(db, request_input=request_input, user_id=user.user_id)
    return DataResponse().success_response(data=data)


@router.get('/', response_model=DataResponse[GetFileResponse])
def get_file(id: str):
    data = FileElasticService.get_file(id=id)
    return DataResponse().success_response(data=data)


@router.get('/list-file', response_model=DataResponse[GetListFileResponse])
def get_list_file(size: int = 5):
    data = FileElasticService.get_list_file(size = size)
    return DataResponse().success_response(data=data)


@router.post('/search', response_model=DataResponse[SearchFileMappingResponse])
def search_content_file(db: Session = Depends(db_session),
                                  *,
                                  request_input: SearchFileRequest):
    data, pagination = FileElasticService.search_content(db, request_input)
    return PagingDataResponse().success_response(data=data, pagination=pagination)
