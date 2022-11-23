# -*- coding: utf-8 -*-

# YADRO Tatlin Unified Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.endpoints as eps
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.models.task import Task
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.exception import TatlinClientError

try:
    from typing import List, Optional
except ImportError:
    List = Optional = None


class Subnet:

    _cache = {}

    @classmethod
    def clear_cache(cls):
        cls._cache = {}

    def __init__(self, client, **data):
        self._client = client
        self._data = data

    @property
    def id(self):  # type: () -> str
        rv = self._data.get('id')
        if rv is None:
            raise AttributeError(
                'Subnet object has no id value'
            )
        return rv

    @property
    def ip_end(self):  # type: () -> Optional[str]
        try:
            return self._data.get('ips', [None, None])[1]
        except IndexError:
            raise TatlinClientError('Unknown ip range format for subnet')

    @property
    def ip_start(self):  # type: () -> Optional[str]
        try:
            return self._data.get('ips', [None, None])[0]
        except IndexError:
            raise TatlinClientError('Unknown ip range format for subnet')

    @property
    def name(self):  # type: () -> str
        return self._data.get('name')

    @property
    def resources(self):  # type: () -> List['models.resource.Resource']
        rv = []

        resources = self._cache.get('resources')
        if resources is None:
            resources = self._cache['resources'] = \
                self._client.get_resources()

        for resource in resources:
            if resource.id in (self._data['resources'] or []):
                rv.append(resource)

        return rv

    def load(self):  # type: () -> None
        self._data.get('{ep}/{id}'.format(
            ep=eps.PERSONALITIES_SUBNETS_ENDPOINT,
            id=self.id,
        ))

        self.clear_cache()

    def update(self, ip_start=None, ip_end=None):  # type: (str, str) -> Task
        task_data = self._client.put(
            path='{ep}/update/{id}'.format(
                ep=eps.DASHBOARD_SUBNETS_ENDPOINT,
                id=self.id,
            ),
            body={
                'name': self.name,
                'ips': [
                    ip_start or self.ip_start,
                    ip_end or self.ip_end,
                ],
            }
        ).json

        return Task(client=self._client, **task_data)

    def remove(self):  # type: () -> Task
        task_data = self._client.put('{ep}/delete/{id}'.format(
            ep=eps.DASHBOARD_SUBNETS_ENDPOINT,
            id=self.id,
        )).json

        return Task(client=self._client, **task_data)

    def __eq__(self, other):
        if isinstance(other, Subnet):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
