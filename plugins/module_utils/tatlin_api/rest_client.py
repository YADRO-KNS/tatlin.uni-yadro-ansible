# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    from typing import Dict, Union
except ImportError:
    # Satisfy Python 2 which doesn't have typing.
    Dict = Union = None

from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import (
    RESTClientError,
    RESTClientNotFoundError,
    RESTClientRequestError,
    RESTClientConnectionError
)

import json
from ansible.module_utils.urls import open_url
from ansible.module_utils.six.moves.urllib.parse import urlencode
from ansible.module_utils.six.moves.http_client import HTTPResponse
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


def build_url(base, path, query_params=None):  # type: (str, str, Dict) -> str
    url = "{0}/{1}".format(base.rstrip("/"), path.lstrip("/"))
    if query_params:
        url += "?" + urlencode(query_params)
    return url


AUTH_BASIC = 'basic'
AUTH_SESSION = 'session'


class RestClient:

    def __init__(
        self,
        base_url,  # type: str
        username=None,  # type: str
        password=None,  # type: str
        validate_certs=True,  # type: bool
        login_path=None,  # type: str
        timeout=10,  # type: int
        auth_method=AUTH_SESSION,
    ):  # type: (...) -> None

        self._username = username
        self._password = password
        self._login_path = login_path
        self._auth_key = None
        self._token = None
        self._auth_method = auth_method

        if "://" in base_url:
            self._protocol, self._host = base_url.split("://")
        else:
            self._protocol = "https"
            self._host = base_url

        self.validate_certs = validate_certs
        self.timeout = timeout

    def authorize(self, username=None, password=None, auth=None):
        raise NotImplementedError

    def set_host(self, host):  # type: (str) -> None
        self._host = host

    def get_host(self):  # type: () -> str
        return self._host

    def make_request(
        self, path, method, query_params=None, body=None, headers=None,
    ):  # type: (str, str, Dict, Union[Dict, bytes], Dict) -> RestResponse

        request_kwargs = {
            "follow_redirects": "all",
            "force_basic_auth": False,
            "headers": self._get_headers(),
            "method": method,
            "timeout": self.timeout,
            "use_proxy": True,
            "validate_certs": self.validate_certs,
        }

        if body:
            if isinstance(body, dict) or isinstance(body, list):
                request_kwargs["headers"]["Content-Type"] = "application/json"
                request_body = json.dumps(body)
            elif isinstance(body, bytes):
                request_kwargs["headers"]["Content-Type"] = "application/octet-stream"
                request_body = body
            else:
                raise RESTClientError(
                    "Unsupported body type: {0}".format(type(body)))
        else:
            request_body = None

        if headers:
            request_kwargs["headers"].update(headers)

        url = build_url(self.base_url, path, query_params=query_params)
        response = self._make_request(url, request_body, **request_kwargs)
        return RestResponse(response)

    def _make_request(self, url, request_body, **request_kwargs):
        try:
            response = open_url(url=url, data=request_body, **request_kwargs)
        except HTTPError as e:
            if e.code == 404:
                raise RESTClientNotFoundError('Not found: {0}'.format(e.url))
            else:
                try:
                    msg = json.load(e)
                except ValueError:
                    msg = str(e)
                raise RESTClientRequestError(
                    'Request finished with error: {0}'.format(msg))
        except (URLError, SSLValidationError, ConnectionError) as e:
            raise RESTClientConnectionError(
                'Cannot connect to server: {0}'.format(str(e)))
        else:
            return response

    def get(self, path, query_params=None, headers=None):
        # type: (str, Dict, Dict) -> RestResponse
        return self.make_request(
            path, method="GET", query_params=query_params, headers=headers)

    def post(self, path, body=None, headers=None):
        # type: (str, Union[Dict, bytes], Dict) -> RestResponse
        return self.make_request(
            path, method="POST", body=body, headers=headers)

    def delete(self, path, headers=None):
        # type: (str, Dict) -> RestResponse
        return self.make_request(
            path, method="DELETE", headers=headers)

    def patch(self, path, body=None, headers=None):
        # type: (str, Dict, Dict) -> RestResponse
        return self.make_request(
            path, method="PATCH", body=body, headers=headers)

    def put(self, path, body=None, headers=None):
        # type: (str, Dict, Dict) -> RestResponse
        return self.make_request(
            path, method="PUT", body=body, headers=headers)

    def _get_headers(self):
        headers = {}

        if self._token:
            headers['X-Auth-Token'] = self._token
        elif self._auth_key:
            headers['Authorization'] = self._auth_key

        return headers

    @property
    def base_url(self):
        return "{0}://{1}".format(self._protocol, self._host)


class RestResponse:

    def __init__(self, response):  # type: (HTTPResponse) -> None
        self._response = response
        self._body = self._response.read()

    @property
    def json(self):  # type: () -> Dict
        try:
            return json.loads(self._body)
        except ValueError:
            raise ValueError("Unable to parse json")

    @property
    def headers(self):  # type: () -> Dict
        return dict(self._response.headers)

    @property
    def status_code(self):  # type: () -> int
        return self._response.getcode()

    @property
    def is_success(self):  # type: () -> bool
        return self.status_code in (200, 201, 202, 204)
