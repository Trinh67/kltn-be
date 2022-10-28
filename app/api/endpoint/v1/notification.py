import logging

from h11 import Data
from app.helper.db import db_session
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.dto.core.auth import UserDTO
from app.dto.core.notification import GetListNotificationResponse
from app.helper.base_response import DataResponse
from app.helper.middleware import get_current_user
from app.service.notification import NotificationService



router = APIRouter()

_logger = logging.getLogger(__name__)


@router.get('/', response_model=DataResponse[GetListNotificationResponse])
def get_list_notification(db: Session = Depends(db_session), user: UserDTO = Depends(get_current_user)):
    data = NotificationService.get_list_notification(db, user=user)
    return DataResponse().success_response(data=data)

@router.get('/make-all-read',response_model=DataResponse[None])
def make_all_read(db: Session = Depends(db_session), user: UserDTO = Depends(get_current_user)):
    data = NotificationService.make_all_read(db, user=user)
    return DataResponse().success_response(data=None)
