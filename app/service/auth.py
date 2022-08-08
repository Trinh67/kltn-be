import os
from datetime import timedelta, datetime

import google.auth
from google.auth.transport import requests
from google.oauth2 import id_token
from jose import JWTError
from sqlalchemy.orm import Session

from app.dto.core.auth import TokenDTO
from app.helper.custom_exception import UnauthorizedException
from app.helper.jwt import create_jwt, get_pay_load
from app.model import User
from setting import setting


class AuthService:

    @classmethod
    def decode_token(cls, token_id):
        decoded_token = id_token.verify_oauth2_token(token_id, requests.Request(), setting.GOOGLE_CLIENT_ID)
        if decoded_token['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise UnauthorizedException
        return decoded_token

    @classmethod
    def create_token(cls, user: User, expire_minutes):
        return create_jwt(
            data={
                'sub': user.email,
                'user_name': user.name,
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(minutes=expire_minutes),
                'iss': 'kltn.ml'
            }
        )

    @classmethod
    def exchange_access_token(cls, db: Session, refresh_token: str):
        try:
            decoded_token = get_pay_load(refresh_token)
        except JWTError:
            raise UnauthorizedException

        user = db.query(User).filter(User.email == decoded_token['sub']).first()
        return TokenDTO(
            access_token=cls.create_token(user, setting.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    @classmethod
    def login_with_google(cls, db: Session, token_id):
        try:
            decoded_token = cls.decode_token(token_id=token_id)
        except ValueError:
            raise UnauthorizedException

        if 'email' not in decoded_token:
            raise UnauthorizedException

        email = decoded_token['email']
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User()
            user.email = email
            user.user_id = decoded_token.get('sub')
            user.name = decoded_token.get('name')
            user.avatar_url = decoded_token.get('picture')
            db.add(user)
            db.commit()

        access_token = cls.create_token(user, setting.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token = cls.create_token(user, setting.REFRESH_TOKEN_EXPIRE_MINUTES)
        return TokenDTO(access_token=access_token, refresh_token=refresh_token)
