import logging
import time
from enum import Enum
from http import HTTPStatus

import requests
from app.adapter.base import detect_slow_call
from app.dto.core.auth import FacebookUserResponse
from app.helper.custom_exception import FacebookServiceCallException
from setting import setting

_logger = logging.getLogger(__name__)


class FacebookServiceStatus(str, Enum):
    SUCCESS = '200'


class FacebookService:
    _api_base_url = setting.FACEBOOK_SERVICE_API_BASE_URL

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
                    "Calling Facebook Service URL: %s, request_param %s, request_payload %s, http_code: %s, response: %s" %
                    (url, str(query_params), str(json_data), str(resp.status_code), resp.text))
            return resp
        except Exception as e:
            _logger.warning(f"Calling Facebook Service URL: {url},"
                            f" request_params {str(query_params)}, request_body {str(json_data)},"
                            f" error {str(e)}")
            raise e

    @classmethod
    def get_user_info(cls, token: str) -> FacebookUserResponse:

        try:
            resp = cls.call(
                method='GET',
                url_path=f'/me?fields=id,name,picture,email&access_token={token}'
            )
        except Exception as e:
            _logger.exception(e)
            raise FacebookServiceCallException('api get_user')

        raw_json = resp.json()
        if resp.status_code == HTTPStatus.OK:
            data = dict()
            data['id'] = raw_json.get('id')
            data['name'] = raw_json.get('name')
            data['email'] = raw_json.get('email')
            data['avatar_url'] = raw_json.get('picture').get('data').get('url')
            return FacebookUserResponse.parse_obj(data)

        raise FacebookServiceCallException('api get_user')
