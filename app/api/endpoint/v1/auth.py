from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dto.core.auth import TokenDTO, LoginGoogleDTO, ExchangeAccessTokenDTO, UserDTO
from app.helper.base_response import DataResponse
from app.helper.db import db_session
from app.helper.middleware import get_current_user
from app.service.auth import AuthService

router = APIRouter()


@router.post('/login-google', response_model=DataResponse[TokenDTO])
def login_with_google(login_google_dto: LoginGoogleDTO, db: Session = Depends(db_session)):
    data = AuthService.login_with_google(db, login_google_dto.token_id)
    return DataResponse().success_response(data)


@router.get('/current-user', response_model=DataResponse[UserDTO])
def get_user_info(current_user=Depends(get_current_user)):
    return DataResponse().success_response(current_user)


@router.post('/exchange-access-token', response_model=DataResponse[TokenDTO])
def exchange_access_token(exchange_access_token_dto: ExchangeAccessTokenDTO,
                          db: Session = Depends(db_session)):
    data = AuthService.exchange_access_token(db, exchange_access_token_dto.refresh_token)
    return DataResponse().success_response(data)
