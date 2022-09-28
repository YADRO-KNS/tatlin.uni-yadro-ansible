# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from uuid import uuid4
import ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints as eps
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.models.resource import (
    ResourceBase, ResourceBlock, ResourceFile, RESOURCE_TYPE,
)
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.models.task import Task
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.utils import to_bytes

try:
    from typing import List, Union, Dict, Tuple, Optional, TYPE_CHECKING
except ImportError:
    List = Union = Dict = Tuple = Optional = TYPE_CHECKING = None

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
        rv = []

        drive_id_list = self._data.get('disks_list', [])
        for drive in self.drive_group.drives:
            if drive.id in drive_id_list:
                rv.append(drive)
        return rv

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
    ):  # type: (...) -> Task

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

        return Task(client=self._client, **task_data)

    def create_resource_file(
        self,
        name,  # type: str
        resource_type,  # type: str
        size,  # type: Union[int, str]
        name_template=None,  # type: str
        read_cache=True,  # type: bool
        write_cache=True,  # type: bool
        ports=None,  # type: List['models.port.Port']
        subnets=None,  # type: List['models.subnet.Subnet']
        users=None,  # type: List[Tuple['models.user.User', str]]
        user_groups=None,  # type: List[Tuple['models.user_group.UserGroup', str]]
    ):  # type: (...) -> Task
        """
        users: List of tuples containing two elements: (user, permission).
            Allowed permissions: 'r' - read, 'rw' - 'read/write'
        user_groups: List of tuples containing two elements:
            (user_group, permission).
            Allowed permissions: 'r' - read, 'rw' - 'read/write'
        """

        if resource_type not in (RESOURCE_TYPE.NFS, RESOURCE_TYPE.CIFS):
            raise TatlinClientError(
                'Unknown file resource type: {0}'.format(resource_type)
            )

        if isinstance(size, str):
            size = to_bytes(size)

        acl = []

        if users is not None:
            ResourceFile.validate_users(users)

            for user, permissions in users:
                acl.append({
                    'principal': {'kind': 'user', 'name': user.name},
                    'permissions': ResourceFile.get_permissions_for_request(
                        permissions)
                })

        if user_groups is not None:
            ResourceFile.validate_user_groups(user_groups)

            for group, permissions in user_groups:
                acl.append({
                    'principal': {'kind': 'group', 'name': group.name},
                    'permissions': ResourceFile.get_permissions_for_request(
                        permissions)
                })

        port_names = None
        if ports is not None:
            port_names = [{'port': port.name} for port in ports]

        subnet_ids = None
        if subnets is not None:
            subnet_ids = [subnet.id for subnet in subnets]

        if self._file_resource_legacy():
            return self._create_file_resource_legacy(
                name=name,
                name_template=name_template,
                resource_type=resource_type,
                size=size,
                read_cache=read_cache,
                write_cache=write_cache,
                port_names=port_names,
                acl=acl,
                subnet_ids=subnet_ids,
            )

        resource_names = self._client.post(
            path=eps.DASHBOARD_RESOURCES_ENDPOINT + '/file/create',
            body={
                'bulk_params': {
                    'names': None,
                    'templates': [{
                        'nameTemplate': name,
                        'params': name_template,
                    }],
                },
                'type': resource_type,
                'poolId': self.id,
                'size': size,
                'cached': 'true',
                'rCacheMode': 'enabled' if read_cache else 'disabled',
                'wCacheMode': 'enabled' if write_cache else 'disabled',
                'ports': port_names,
                'acl': acl or None,
                'subnets': subnet_ids,
            }
        ).json

        task_data = self._client.put(
            path=eps.DASHBOARD_RESOURCES_ENDPOINT + '/file/create',
            body={
                'bulk_params': {'names': resource_names},
                'type': resource_type,
                'poolId': self.id,
                'size': size,
                'cached': 'true',
                'rCacheMode': 'enabled' if read_cache else 'disabled',
                'wCacheMode': 'enabled' if write_cache else 'disabled',
                'ports': port_names,
                'acl': acl or None,
                'subnets': subnet_ids,
            }
        ).json

        return Task(client=self._client, **task_data)

    def get_drive_ids(self):
        return self._data.get('disks_list', [])

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

    def _file_resource_legacy(self):  # type: () -> bool
        """Tatlin 2.6 does not support bulk file resources creation"""
        major, minor = self._client.system_version.split('.')[:2]
        return (int(major), int(minor)) < (2, 7)

    def _create_file_resource_legacy(
        self,
        name,  # type: str
        name_template,  # type: Union[str, None]
        resource_type,  # type: str
        size,  # type: int
        read_cache,  # type: bool
        write_cache,  # type: bool
        port_names,  # type: List[str]
        acl,  # type: List[Dict]
        subnet_ids,  # type: List[str]
    ):  # type(...) -> Task
        if name_template is not None:
            raise TatlinClientError(
                'Bulk resource creation is not allowed for Tatlin <= 2.6'
            )

        task_data = self._client.put(
            path=eps.DASHBOARD_RESOURCES_ENDPOINT + '/file/create',
            body={
                'id': str(uuid4()),
                'name': name,
                'type': resource_type,
                'poolId': self.id,
                'size': size,
                'cached': 'true',
                'rCacheMode': 'enabled' if read_cache else 'disabled',
                'wCacheMode': 'enabled' if write_cache else 'disabled',
                'ports': port_names,
                'acl': acl or None,
                'subnets': subnet_ids,
            }
        ).json

        return Task(client=self._client, **task_data)

    def __eq__(self, other):
        if isinstance(other, Pool):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
