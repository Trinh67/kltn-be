from sqlalchemy.orm import Session
from app.helper.db import db_session
from fastapi import APIRouter, Depends
from app.helper.middleware import get_current_user

from app.dto.core.auth import UserDTO
from app.service.user import UserService
from app.dto.core.user import GetListUserResponse
from app.helper.base_response import DataResponse

router = APIRouter()


@router.get('/list-user', response_model=DataResponse[GetListUserResponse])
def get_list_user(db: Session = Depends(db_session), user:UserDTO = Depends(get_current_user)):
    data = UserService.get_list_user(db, user=user)
    return DataResponse().success_response(data=data)