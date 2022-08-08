from datetime import datetime
from jose import jwt, JWTError
from pydantic import ValidationError, BaseModel

from app.helper.custom_exception import UnauthorizedException
from setting import setting


class TokenData(BaseModel):
    sub: str
    exp: datetime


def get_pay_load(token):
    try:
        return jwt.decode(
            token=token,
            key=setting.JWT_SECRET_KEY,
            algorithms=setting.JWT_ALGORITHM
        )
    except ValidationError:
        raise UnauthorizedException
    except JWTError:
        raise UnauthorizedException


def create_jwt(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, setting.JWT_SECRET_KEY, algorithm=setting.JWT_ALGORITHM)
    return encoded_jwt
