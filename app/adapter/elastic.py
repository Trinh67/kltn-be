import logging
import time
from enum import Enum
from http import HTTPStatus

import requests
from app.adapter.base import detect_slow_call
from app.dto.elastic.file import CreateFileResponse, SearchFileResponse
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
    def search_content(cls, content: str, size: int = 5) -> SearchFileResponse:
        parse_content = content.split('"')
        json_data = {
                    "query": {
                        "bool": {
                            "should": [
                                {
                                "match": {
                                    "content": content
                                }
                                }
                            ]
                        }
                    },
                    "size": size
                }
        if len(parse_content) > 1:
            json_data = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "content": parse_content[1]
                                }
                            }
                        ],
                        "should": [
                            {
                                "match": {
                                    "content": parse_content[0]
                                }
                            },
                            {
                                "match": {
                                    "content": parse_content[2]
                                }
                            }
                        ]
                    }
                },
                "size": size
            }
        try:
            resp = cls.call(
                method='GET',
                url_path=f'/document/_search/',
                json_data=json_data
            )
        except Exception as e:
            _logger.exception(e)
            raise ElasticServiceCallException('api search_content')

        raw_json = resp.json().get('hits')
        if resp.status_code == HTTPStatus.OK:
            data = dict()
            data['total'] = raw_json.get('total').get('value')
            data['files'] = [file.get('_id') for file in raw_json.get('hits')]
            return SearchFileResponse.parse_obj(data)

        raise ElasticServiceCallException('api search_content')
    
    @classmethod
    def create_file(cls, content: str) -> CreateFileResponse:

        try:
            resp = cls.call(
                method='POST',
                url_path=f'/document/_doc/',
                json_data={
                    'content': content
                }
            )
        except Exception as e:
            _logger.exception(e)
            raise ElasticServiceCallException('api create_file')

        raw_json = resp.json()
        if resp.status_code == HTTPStatus.CREATED:
            data = dict()
            data['id'] = raw_json.get('_id')
            return CreateFileResponse.parse_obj(data)

        raise ElasticServiceCallException('api create_file')
