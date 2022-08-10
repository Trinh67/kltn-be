import logging
from typing import Optional

from fastapi import Depends
from fastapi.security import APIKeyHeader, HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.orm import Session

from app.dto.core.auth import UserDTO
from app.helper.custom_exception import UnauthorizedException
from app.helper.db import db_session
from app.helper.jwt import TokenData, get_pay_load
from app.model import User

LOGGING_METHOD = ['POST', 'PUT', 'DELETE']
HEALTH_CHECK_API = 'health/check'

_logger = logging.getLogger(__name__)
authorize_header = APIKeyHeader(name='authorization', auto_error=False)


def get_current_user(
        access_token: Optional[str] = Depends(authorize_header),
        db: Session = Depends(db_session)
) -> Optional[UserDTO]:
    scheme, token = get_authorization_scheme_param(access_token)
    if scheme.lower() != "bearer":
        raise UnauthorizedException

    token_data = TokenData(**get_pay_load(token))

    user = User.q(db, User.user_id == token_data.sub).first()

    if not user:
        raise UnauthorizedException

    result = UserDTO.from_orm(user)

    return result
