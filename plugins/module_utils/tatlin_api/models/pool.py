# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints as eps
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.models.resource import (
    ResourceBase, ResourceBlock, ResourceFile, RESOURCE_TYPE,
)
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.utils import to_bytes

try:
    from typing import List, Union, Dict, Optional, TYPE_CHECKING
except ImportError:
    List = Union = Dict = Optional = TYPE_CHECKING = None

if TYPE_CHECKING:
    from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api import models


class PROVISION_TYPE:
    THIN = 'thin'
    THICK = 'thick'


class Pool:

    def __init__(self, client, drive_group, **pool_data):
        self._client = client
        self._data = pool_data
        self._ep = '{0}/{1}'.format(eps.HEALTH_POOLS_ENDPOINT, self.id)

        self.drive_group = drive_group

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
    def capacity_used(self):  # type: () -> int
        rv = int(self._data['used']) \
            if self._data.get('used') is not None else None
        return rv

    @property
    def critical_threshold(self):  # type: () -> int
        return self._data.get('critical_alert_threshold')

    @property
    def drives(self):  # type: () -> List['Drive']
        drive_id_list = self._data.get('disks_list', [])
        return [self.drive_group.get_drive(_id) for _id in drive_id_list]

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
    def protection(self):  # type: () -> str
        return self._data.get('protection')

    @property
    def provision(self):  # type: () -> Optional[str]
        if self._data.get('thinProvision') is None:
            return None

        rv = PROVISION_TYPE.THIN if \
            self._data['thinProvision'] else PROVISION_TYPE.THICK
        return rv

    @property
    def spare_count(self):  # type: () -> int
        rv = int(self._data['spare']) \
            if self._data.get('spare') is not None else None
        return rv

    @property
    def status(self):  # type: () -> str
        return self._data.get('status')

    @property
    def stripe_size(self):  # type: () -> int
        return self._data.get('stripe_size')

    @property
    def warning_threshold(self):  # type: () -> int
        return self._data.get('soft_alert_threshold')

    def create_resource_block(
        self,
        name,  # type: str
        size,  # type: Union[int, str]
        size_format=None,  # type: str
        name_template=None,  # type: str
        read_cache=True,  # type: bool
        write_cache=True,  # type: bool
        warning_threshold=None,  # type: int
        ports=None,  # type: List['models.port.Port']
        hosts=None,  # type: List['models.host.Host']
        host_groups=None,  # type: List['models.host_group.HostGroup']
    ):  # type: (...) -> int

        if isinstance(size, str):
            size = to_bytes(size)

        port_names = None
        host_names = None
        host_group_names = None

        if ports is not None:
            port_names = [port.name for port in ports]

        if hosts is not None:
            host_names = [host.name for host in hosts]

        if host_groups is not None:
            host_group_names = [group.name for group in host_groups]

        resource_names = self._client.post(
            path=eps.DASHBOARD_RESOURCES_ENDPOINT + '/block/create',
            body={
                'templates': [{'nameTemplate': name, 'params': name_template}],
                'poolId': self.id,
                'size': size,
                'lbaFormat': size_format,
                'cached': 'true',
                'rCacheMode': 'enabled' if read_cache else 'disabled',
                'wCacheMode': 'enabled' if write_cache else 'disabled',
                'alert_threshold': warning_threshold,
                'ports': port_names,
                'hosts': host_names,
                'groups': host_group_names,
            }
        ).json

        task_data = self._client.put(
            path=eps.DASHBOARD_RESOURCES_ENDPOINT + '/block/create',
            body={
                'names': resource_names,
                'poolId': self.id,
                'size': size,
                'lbaFormat': size_format,
                'cached': 'true',
                'rCacheMode': 'enabled' if read_cache else 'disabled',
                'wCacheMode': 'enabled' if write_cache else 'disabled',
                'alert_threshold': warning_threshold,
                'ports': port_names,
                'hosts': host_names,
                'groups': host_group_names,
            }
        ).json

        return task_data['id']

    @staticmethod
    def _get_permissions_for_request(permissions):
        # type: (str) -> List[str]
        if permissions == 'r':
            return ['read']
        elif permissions == 'rw':
            return ['read', 'write']

        raise TatlinClientError(
            'Unknown permissions: {0}'.format(permissions)
        )

    def get_resource(self, name):
        # type: (str) -> Optional[Union[ResourceBlock, ResourceFile]]
        for resource in self.get_resources():
            if resource.name == name:
                return resource
        return None

    def get_resources(self):
        # type: () -> List[Union[ResourceBlock, ResourceFile]]
        rv = []

        ResourceBase.clear_cache()

        resources_data = self._client.get(
            eps.HEALTH_PERSONALITIES_ENDPOINT
        ).json

        for resource_data in resources_data:
            if resource_data['poolId'] == self.id:
                resource_type = resource_data.get('type')
                if resource_type == RESOURCE_TYPE.BLOCK:
                    rv.append(ResourceBlock(
                        client=self._client,
                        pool=self,
                        **resource_data
                    ))
                elif resource_type in (RESOURCE_TYPE.NFS, RESOURCE_TYPE.CIFS):
                    rv.append(ResourceFile(
                        client=self._client,
                        pool=self,
                        **resource_data
                    ))
                else:
                    raise TatlinClientError(
                        'Unknown resource type: {0}'.format(resource_type)
                    )
        return rv

    def is_deleting(self):  # type: () -> bool
        return self.status.lower() == 'deleting'

    def is_ready(self):  # type: () -> bool
        return self.status.lower() == 'ready'

    def is_resizing(self):  # type: () -> bool
        return self._data['resizing']

    def load(self):  # type: () -> None
        self._data = self._client.get(self._ep).json

    def remove(self):  # type: () -> None
        if len(self.get_resources()) > 0:
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
