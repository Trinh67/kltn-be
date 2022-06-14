import logging

from fastapi import APIRouter

from app.helper.base_response import ResponseSchemaBase

router = APIRouter()

_logger = logging.getLogger(__name__)


@router.get('/check', response_model=ResponseSchemaBase)
def check_health():
    return ResponseSchemaBase().success_response()
