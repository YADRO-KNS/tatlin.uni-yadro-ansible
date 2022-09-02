# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints as eps
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.utils import get_iscsi_auth_for_request

try:
    from typing import List, Union
except ImportError:
    List = Union = None


class Host:

    def __init__(self, client, **host_data):
        self._client = client
        self._data = host_data

    @property
    def auth(self):  # type: () -> str
        return self._data.get('auth', {}).get('auth_type')

    @property
    def id(self):  # type: () -> str
        return self._data.get('id')

    @property
    def mutual_username(self):  # type: () -> str
        return self._data.get('auth', {}).get('external_name')

    @property
    def name(self):  # type: () -> str
        return self._data.get('name')

    @property
    def port_type(self):  # type: () -> str
        rv = self._data.get('port_type')
        if rv == 'iscsi':
            return 'eth'
        return rv

    @property
    def ports(self):  # type: () -> List[str]
        return self._data.get('initiators') or []

    @property
    def tags(self):  # type: () -> List[str]
        return self._data.get('tags', [])

    @property
    def username(self):  # type: () -> str
        return self._data.get('auth', {}).get('internal_name')

    def load(self):  # type: () -> None
        self._data = self._client.get(
            '{ep}/{id}'.format(
                ep=eps.PERSONALITIES_HOSTS_ENDPOINT,
                id=self.id
            )
        ).json

    def update(
        self,
        auth=None,  # type: str
        username=None,  # type: str
        password=None,  # type: str
        mutual_username=None,  # type: str
        mutual_password=None,  # type: str
        ports=None,  # type: Union[str, List[str]]
        tags=None,  # type: Union[str, List[str]]
    ):  # type: (...) -> None

        auth_body = None

        if any(param is not None for param in [
            auth, username, password, mutual_username, mutual_password
        ]):
            auth_body = get_iscsi_auth_for_request(
                auth or self.auth,
                username or self.username,
                password,
                mutual_username or self.mutual_username,
                mutual_password,
            )

        ports = [ports] if isinstance(ports, str) else ports
        tags = [tags] if isinstance(tags, str) else tags

        self._client.post(
            path=eps.PERSONALITIES_HOSTS_ENDPOINT,
            body={
                'id': self.id,
                'name': self.name,
                'port_type': self._data.get('port_type'),
                'initiators': ports if ports is not None else self.ports,
                'tags': tags if tags is not None else self.tags,
                'auth': auth_body,
            }
        )

        self.load()
