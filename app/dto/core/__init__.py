from typing import Dict, Optional
import logging
from humps import decamelize

from app.dto.base import CamelBaseModel

_logger = logging.getLogger(__name__)


class UpdateModel(CamelBaseModel):
    _included_fields: Optional[Dict] = dict()

    def __init__(self, **kwargs):
        included_fields = dict()
        for key in kwargs:
            decamelize_key = decamelize(key)
            included_fields.__setitem__(decamelize_key, ...)

        super().__init__(**kwargs)
        object.__setattr__(self, '_included_fields', included_fields)

    @property
    def included_fields(self):
        return self._included_fields

    def dict(self, exclude_unset: Optional[bool] = True, **kwargs):
        if exclude_unset:
            temp_dict = self._included_fields.copy()
            if 'include' in kwargs:
                for k in self._included_fields.keys():
                    if k not in kwargs.get('include').keys():
                        temp_dict.pop(k)

                kwargs.pop('include')

            return super().dict(include=temp_dict, **kwargs)

        return super().dict(**kwargs)
