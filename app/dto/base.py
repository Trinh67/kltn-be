from typing import Optional, List, Union, Any
import time
from humps import camelize, decamelize, pascalize
from pydantic import BaseModel
from pydantic.utils import GetterDict
from datetime import datetime


class OpenApiResponseModel:
    http_code: str
    description: str
    code: int
    message: str
    data: Optional[dict]

    def __init__(self, http_code: str, description: str, code: int, message: str, data: Optional[Union[dict, List]] = None):
        self.http_code = http_code
        self.description = description
        self.code = code
        self.message = message
        self.data = data


class ConvertTimestamp(GetterDict):
    def get(self, key: Any, default: Any = None) -> Any:
        decamelize_key = decamelize(key)
        if isinstance(getattr(self._obj, decamelize_key), datetime):
            return time.mktime(getattr(self._obj, decamelize_key).timetuple())
        else:
            return super().get(decamelize_key, default)


class CamelBaseModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True

class PascalBaseModel(BaseModel):
    class Config:
        alias_generator = pascalize
        allow_population_by_field_name = True

