# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints as eps
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.utils import to_bytes

try:
    from typing import List, Union, Dict, Optional
except ImportError:
    List = Union = Dict = Optional = None


class PROVISION_TYPE:
    THIN = 'thin'
    THICK = 'thick'


class Pool:

    def __init__(self, client, drive_group, **pool_data):
        self._client = client
        self._data = pool_data
        self._ep = '{0}/{1}'.format(eps.HEALTH_POOLS_ENDPOINT, self.id)

        self.drive_group = drive_group
        self.resources = []
        self.load_resources()

    @property
    def id(self):  # type: () -> str
        rv = self._data.get('id')
        if rv is None:
            raise AttributeError(
                'Pool object has no id value'
            )
        return rv

    @property
    def name(self):  # type: () -> str
        return self._data.get('name')

    @property
    def status(self):  # type: () -> str
        return self._data.get('status')

    @property
    def provision(self):  # type: () -> Optional[str]
        if self._data.get('thinProvision') is None:
            return None

        rv = PROVISION_TYPE.THIN if \
            self._data['thinProvision'] else PROVISION_TYPE.THICK
        return rv

    @property
    def protection(self):  # type: () -> str
        return self._data.get('protection')

    @property
    def capacity_used(self):  # type: () -> int
        rv = int(self._data['used']) \
            if self._data.get('used') is not None else None
        return rv

    @property
    def capacity_available(self):  # type: () -> int
        rv = int(self._data['available']) \
            if self._data.get('available') is not None else None
        return rv

    @property
    def capacity_failed(self):  # type: () -> int
        rv = int(self._data['failed']) \
            if self._data.get('failed') is not None else None
        return rv

    @property
    def capacity_total(self):  # type: () -> int
        rv = int(self._data['capacity']) \
            if self._data.get('capacity') is not None else None
        return rv

    @property
    def stripe_size(self):  # type: () -> int
        return self._data.get('stripe_size')

    @property
    def drives(self):  # type: () -> List['Drive']
        drive_id_list = self._data.get('disks_list', [])
        return [self.drive_group.get_drive(_id) for _id in drive_id_list]

    @property
    def spare_count(self):  # type: () -> int
        rv = int(self._data['spare']) \
            if self._data.get('spare') is not None else None
        return rv

    @property
    def warning_threshold(self):  # type: () -> int
        return self._data.get('soft_alert_threshold')

    @property
    def critical_threshold(self):  # type: () -> int
        return self._data.get('critical_alert_threshold')

    def is_deleting(self):  # type: () -> bool
        return self.status.lower() == 'deleting'

    def is_ready(self):  # type: () -> bool
        return self.status.lower() == 'ready'

    def is_resizing(self):  # type: () -> bool
        return self._data['resizing']

    def load(self):  # type: () -> None
        self._data = self._client.get(self._ep).json
        self.load_resources()

    def load_resources(self):
        self.resources = []

        resources_data = self._client.get(
            eps.HEALTH_PERSONALITIES_ENDPOINT
        ).json

        for item in resources_data:
            if item['poolId'] == self.id:
                # TODO: Implement as objects after Resource class implementation
                self.resources.append(item)

    def remove(self):  # type: () -> None
        if len(self.resources) > 0:
            raise TatlinClientError(
                'It is prohibited to remove pool with existing resources'
            )

        self._client.delete(self._ep)

    def set_drives_count(self, drives_count):  # type: (int) -> None
        if drives_count <= len(self.drives):
            raise TatlinClientError(
                'New drives count should be grater than current. '
                'Current: {0}. Requested: {1}'.format(
                    len(self.drives), drives_count)
            )

        self._client.put(self._ep + '/resize', body={'disks': drives_count})
        self.load()

    def set_size(self, size):  # type: (Union[str, int]) -> None
        if isinstance(size, str):
            size = to_bytes(size)

        if size <= self.capacity_total:
            raise TatlinClientError(
                'New pool size should be grater than current. '
                'Current: {0}. Requested: {1}'.format(
                    self.capacity_total, size)
            )

        self._client.put(self._ep + '/resize', body={'bytes': str(size)})
        self.load()

    def set_spare_count(self, spare_count):  # type: (int) -> None
        self._client.put(self._ep, body={'spare': str(spare_count)})
        self.load()

    def set_thresholds(
        self,
        warning_threshold=None,
        critical_threshold=None,
    ):  # type: (...) -> None

        if warning_threshold is None and critical_threshold is None:
            raise TypeError(
                'At least one argument must be provided'
            )

        if self.provision == 'thick':
            raise TatlinClientError(
                'It is prohibited to set thresholds '
                'for pool with thick provision'
            )

        req_body = {}
        if warning_threshold is not None:
            req_body['soft_alert_threshold'] = warning_threshold
        if critical_threshold is not None:
            req_body['critical_alert_threshold'] = critical_threshold

        self._client.put(self._ep + '/alerts', body=req_body)
        self.load()

    def __eq__(self, other):
        if isinstance(other, Pool):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
