# -*- coding: utf-8 -*-

# YADRO Tatlin Unified Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.endpoints as eps
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.models.host import Host

try:
    from typing import List, Union
except ImportError:
    List = Union = None


class HostGroup:

    def __init__(self, client, **host_group_data):
        self._client = client
        self._data = host_group_data

    @property
    def hosts(self):  # type: () -> List[Host]
        rv = []
        for host in self._client.get_hosts():
            if host.id in self._data['host_ids']:
                rv.append(host)
        return rv

    @property
    def id(self):  # type: () -> str
        rv = self._data.get('id')
        if rv is None:
            raise AttributeError(
                'HostGroup object has no id value'
            )
        return rv

    @property
    def name(self):  # type: () -> str
        return self._data.get('name')

    @property
    def tags(self):  # type: () -> List[str]
        return self._data.get('tags') or []

    def get_resources(self):  # type: () -> List
        rv = []
        for resource in self._client.get_resources():
            if self in resource.host_groups:
                rv.append(resource)
        return rv

    def load(self):  # type: () -> None
        self._data = self._client.get(
            '{ep}/{id}'.format(
                ep=eps.PERSONALITIES_HOST_GROUPS_ENDPOINT,
                id=self.id,
            )
        ).json

    def set_hosts(self, hosts):  # type: (Union[List[Host], Host]) -> None
        if isinstance(hosts, Host):
            hosts = [hosts]

        self._client.post(
            path=eps.PERSONALITIES_HOST_GROUPS_ENDPOINT,
            body={
                'id': self.id,
                'name': self.name,
                'host_ids': [host.id for host in hosts],
                'tags': self._data['tags'],
            }
        )

        self.load()

    def set_tags(self, tags):  # type: (Union[List[str], str]) -> None
        if isinstance(tags, str):
            tags = [tags]

        self._client.post(
            path=eps.PERSONALITIES_HOST_GROUPS_ENDPOINT,
            body={
                'id': self.id,
                'name': self.name,
                'host_ids': self._data['host_ids'],
                'tags': tags,
            }
        )

        self.load()

    def __eq__(self, other):
        if isinstance(other, HostGroup):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
