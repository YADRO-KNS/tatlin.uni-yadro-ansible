# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import (
    PERSONALITIES_ENDPOINT, PERSONALITIES_AUTH_ENDPOINT)


ISCSI_AUTH_TYPES = ('none', 'oneway', 'mutual')


class PersonalitiesService:

    def __init__(self, client):
        self._client = client
        self._ep = PERSONALITIES_ENDPOINT
        self._ep_auth = PERSONALITIES_AUTH_ENDPOINT

    def set_iscsi_auth(
        self,
        auth,  # type: str
        username=None,  # type: str
        password=None,  # type: str
        mutual_username=None,  # type: str
        mutual_password=None,  # type: str
    ):
        if auth not in ISCSI_AUTH_TYPES:
            raise TatlinClientError(
                'Unknown iscsi auth type'
            )

        req_body = {'auth_type': auth}
        if auth in ('oneway', 'mutual'):
            if not username or not password:
                raise TatlinClientError(
                    'username and password must be provided '
                    'with auth type {0}'.format(auth)
                )

            req_body.update(internal_name=username,
                            internal_password=password)

        if auth == 'mutual':
            if not all([
                username, password, mutual_username, mutual_password
            ]):
                raise TatlinClientError(
                    'username, password, mutual_username and mutual_password '
                    'must be provided with {0} auth type'.format(auth)
                )

            req_body.update(external_name=mutual_username,
                            external_password=mutual_password)

        self._client.post(path=self._ep_auth, body=req_body)
