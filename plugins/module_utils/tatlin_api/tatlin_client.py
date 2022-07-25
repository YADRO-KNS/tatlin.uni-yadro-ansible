# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    from typing import Optional
except ImportError:
    Optional = None

from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.rest_client import (
    RestClient,
    AUTH_BASIC,
    AUTH_SESSION,
)

from base64 import b64encode
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.auth.auth_service import AuthService
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.osmgr.osmgr_service import OsmgrService
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.notification.notification_service import NotificationService
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError


LOGIN_PATH = 'auth/login'
LOGOUT_PATH = 'auth/logout'


class TatlinClient(RestClient):

    def __init__(
        self,
        base_url,  # type: str
        username=None,  # type: Optional[str]
        password=None,  # type: Optional[str]
        validate_certs=True,  # type: Optional[bool]
        login_path=LOGIN_PATH,  # type: Optional[str]
        timeout=30,  # type: Optional[int]
        auth_method=AUTH_SESSION,  # type: Optional[str]
    ):  # type: (...) -> None

        super(TatlinClient, self).__init__(
            base_url=base_url,
            username=username,
            password=password,
            validate_certs=validate_certs,
            login_path=login_path,
            timeout=timeout,
            auth_method=auth_method,
        )

        self._auth_service = None
        self._osmgr_service = None
        self._notification_service = None

    def __enter__(self):
        self.authorize(self._username, self._password, self._auth_method)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()

    def authorize(
        self,
        username=None,  # type: Optional[str]
        password=None,  # type: Optional[str]
        auth_method=None,  # type: Optional[str]
        login_path=None,  # type: Optional[str]
    ):  # type: (...) -> None

        self._username = username or self._username
        self._password = password or self._password
        self._auth_method = auth_method or self._auth_method
        self._login_path = login_path or self._login_path

        if self._auth_method == AUTH_BASIC:
            self._auth_key = 'Basic {0}'.format(b64encode(
                b':'.join((self._username, self._password))).strip())

        elif self._auth_method == AUTH_SESSION:
            if self._login_path is None:
                raise TatlinAuthorizationError(
                    'No login path was passed for session authorization'
                )

            response = self.post(
                self._login_path,
                body={'name': self._username, 'secret': self._password},
            ).json

            self._token = response['token']
        elif not self._auth_method:
            pass
        else:
            raise TatlinClientError(
                'Unrecognized authentication method ' + auth_method,
            )

    def logout(self):  # type: () -> None
        if self._token:
            self.post(LOGOUT_PATH)

    # Potentially this method can have more arguments.
    # But now only one is needed
    def reconnect(self, host=None):
        self._host = host or self._host
        self.authorize()

    @property
    def auth_service(self):  # type: () -> AuthService
        if not self._auth_service:
            self._auth_service = AuthService(self)
        return self._auth_service

    @property
    def osmgr_service(self):  # type: () -> OsmgrService
        if not self._osmgr_service:
            self._osmgr_service = OsmgrService(self)
        return self._osmgr_service

    @property
    def notification_service(self):  # type: () -> NotificationService
        if not self._notification_service:
            self._notification_service = NotificationService(self)
        return self._notification_service


class TatlinAuthorizationError(Exception):
    pass
