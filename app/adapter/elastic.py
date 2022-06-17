import logging
import time
from enum import Enum
from http import HTTPStatus

import requests
from app.adapter.base import detect_slow_call
from app.dto.elastic.file import GetFileResponse
from app.helper.custom_exception import ElasticServiceCallException
from setting import setting

_logger = logging.getLogger(__name__)


class ElasticServiceStatus(str, Enum):
    SUCCESS = '200'


class ElasticService:
    _api_base_url = setting.ELASTIC_SERVICE_API_BASE_URL

    @classmethod
    def call(cls, method: str, url_path: str, query_params=None, json_data=None, timeout=30, is_slow=False):
        url = cls._api_base_url + url_path
        headers = {'Content-Type': 'application/json'}
        request_at = time.time()
        try:
            resp: requests.Response = requests.request(method, url, params=query_params, json=json_data,
                                                       headers=headers, timeout=timeout)
            detect_slow_call(request_at, url, is_slow, _logger)
            if resp.status_code != HTTPStatus.OK:
                _logger.warning(
                    "Calling Elastic Service URL: %s, request_param %s, request_payload %s, http_code: %s, response: %s" %
                    (url, str(query_params), str(json_data), str(resp.status_code), resp.text))
            return resp
        except Exception as e:
            _logger.warning(f"Calling Elastic Service URL: {url},"
                            f" request_params {str(query_params)}, request_body {str(json_data)},"
                            f" error {str(e)}")
            raise e

    @classmethod
    def get_file(cls, id: int) -> GetFileResponse:

        try:
            resp = cls.call(
                method='GET',
                url_path=f'/document/_doc/{id}'
            )
        except Exception as e:
            _logger.exception(e)
            raise ElasticServiceCallException('api get_file')

        raw_json = resp.json()
        if resp.status_code == HTTPStatus.OK and raw_json.get('code') == ElasticServiceStatus.SUCCESS:
            return GetFileResponse.parse_obj(
                raw_json
            )

        raise ElasticServiceCallException('api get_file')
