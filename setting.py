import os
import json
from telnetlib import AUTHENTICATION
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(verbose=True)


class Setting(BaseSettings):
    ROOT_DIR = os.path.abspath(os.path.join(
        os.path.dirname(__file__)
    ))

    SLOW_SQL_THRESHOLD_MS: int = os.getenv('SLOW_SQL_THRESHOLD', 20000)
    SLOW_SERVICE_CALL_MS: int = os.getenv('SLOW_SERVICE_CALL_MS', 5000)
    ENV: str = os.getenv('ENV', 'local')
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    PROJECT_TITLE: str = 'KLTN BE'
    SQLALCHEMY_DATABASE_URI: str = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI_TEST: str = os.getenv('SQLALCHEMY_DATABASE_URI_TEST')

    # Jaeger
    JAEGER_ENABLED: int = os.getenv('JAEGER_ENABLED', 0)
    JAEGER_AGENT_HOST: str = os.getenv('JAEGER_HOST', "localhost")
    JAEGER_AGENT_PORT: int = os.getenv('JAEGER_PORT', 6831)
    JAEGER_SAMPLING_RATE: float = os.getenv('JAEGER_SAMPLING_RATE', 1 / 2)

    # Data Storage
    DATA_STORAGE: str = '../data/minio'
    ELASTIC_SERVICE_API_BASE_URL: str = os.getenv('ELASTIC_SERVICE_API_BASE_URL', 'http://localhost:9200')
    FACEBOOK_SERVICE_API_BASE_URL: str = os.getenv('FACEBOOK_SERVICE_API_BASE_URL', 'https://graph.facebook.com/v13.0')

    # AUTHENTICATION
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY')
    GOOGLE_CLIENT_ID: str = os.getenv('GOOGLE_CLIENT_ID')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 12 * 60 * 7
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 24 * 60 * 7

setting = Setting()
