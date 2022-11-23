# -*- coding: utf-8 -*-

# YADRO Tatlin Unified Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.endpoints as eps
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.exception import TatlinClientError
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.utils import to_bytes
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.models.task import Task

try:
    from typing import List, Dict, Tuple, Union, TYPE_CHECKING
except ImportError:
    List = Dict = Tuple = Union = TYPE_CHECKING = None

if TYPE_CHECKING:
    from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.models.port import Port
    from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.models.host_group import HostGroup
    from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.models.host import Host
    from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.models.subnet import Subnet
    from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.models.user import User
    from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.models.user_group import UserGroup


class RESOURCE_TYPE:
    BLOCK = 'block'
    NFS = 'nfs'
    CIFS = 'cifs'


class ResourceBase:

    _cache = {}

    @classmethod
    def clear_cache(cls):
        cls._cache = {}

    def __init__(self, client, pool, **data):
        self._client = client
        self._data = data

        self.pool = pool

    @property
    def capacity_total(self):  # type: () -> int
        return self._data.get('size')

    @property
    def capacity_used(self):  # type: () -> int
        return self._data.get('stat', {}).get('used_capacity')

    @property
    def id(self):  # type: () -> str
        rv = self._data.get('id')
        if rv is None:
            raise AttributeError(
                'Resource object has no id value'
            )
        return rv

    @property
    def name(self):  # type: () -> str
        return self._data.get('name')

    @property
    def read_cache(self):  # type: () -> bool
        return self._data['rCacheMode'] == 'enabled'

    @property
    def size_format(self):  # type: () -> str
        return self._data.get('lbaFormat')

    @property
    def status(self):  # type: () -> str
        return self._data.get('status')

    @property
    def type(self):  # type: () -> str
        raise NotImplementedError

    @property
    def warning_threshold(self):
        return self._data.get('alert_threshold')

    @property
    def write_cache(self):  # type: () -> bool
        return self._data['wCacheMode'] == 'enabled'

    @property
    def ports(self):  # type: () -> List['Port']
        rv = []

        self_port_names = [
            item['port'] for item in self._data.get('ports', [])
        ]

        ports = self._cache.get('ports')
        if ports is None:
            ports = self._cache['ports'] = self._client.get_ports()

        for port in ports:
            if port.name in self_port_names:
                rv.append(port)
        return rv

    def load(self):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def _get_resources_mapping(self):  # type: () -> List[Dict]
        rv = self._cache.get('resources_mapping')
        if rv is None:
            rv = self._cache['resources_mapping'] = self._client.get(
                eps.PERSONALITIES_RESOURCE_MAPPING_ENDPOINT
            ).json
        return rv


class ResourceBlock(ResourceBase):

    @property
    def type(self):  # type: () -> str
        return RESOURCE_TYPE.BLOCK

    @property
    def host_groups(self):
        # type: () -> List['HostGroup']

        mapping = self._get_resources_mapping()
        mapped_group_ids = set()

        for item in mapping:
            resource_id = item.get('resource_id')
            host_group_id = item.get('host_group_id')
            if resource_id == self.id and host_group_id is not None:
                mapped_group_ids.add(host_group_id)

        all_groups = self._cache.get('host_groups')
        if all_groups is None:
            all_groups = self._cache['host_groups'] = \
                self._client.get_host_groups()

        return [group for group in all_groups if group.id in mapped_group_ids]

    @property
    def hosts(self):  # type: () -> List['Host']
        mapping = self._get_resources_mapping()
        mapped_host_ids = set()

        for item in mapping:
            resource_id = item.get('resource_id')
            host_id = item.get('host_id')
            if resource_id == self.id and host_id is not None:
                mapped_host_ids.add(host_id)

        all_hosts = self._cache.get('hosts')
        if all_hosts is None:
            all_hosts = self._cache['hosts'] = self._client.get_hosts()

        return [host for host in all_hosts if host.id in mapped_host_ids]

    @property
    def subnets(self):  # type: () -> List
        return []

    @property
    def users(self):  # type: () -> List
        return []

    @property
    def user_groups(self):  # type: () -> List
        return []

    def load(self):  # type: () -> None
        self._data = self._client.get('{ep}/block/{id}'.format(
            ep=eps.PERSONALITIES_ENDPOINT,
            id=self.id,
        )).json

    def update(
        self,
        size=None,  # type: Union[int, str]
        read_cache=None,  # type: bool
        write_cache=None,  # type: bool
        warning_threshold=None,  # type: int
        ports=None,  # type: List['Port']
        hosts=None,  # type: List['Host']
        host_groups=None,  # type: List['HostGroup']
    ):  # type: (...) -> None

        if size is not None and isinstance(size, str):
            size = to_bytes(size)

        req_body = {}

        if size is not None:
            req_body['new_size'] = size

        if read_cache is not None:
            req_body['rCacheMode'] = 'enabled' if read_cache else 'disabled'

        if write_cache is not None:
            req_body['wCacheMode'] = 'enabled' if write_cache else 'disabled'

        if warning_threshold is not None:
            req_body['alert_threshold'] = warning_threshold

        if len(req_body) > 0:
            self._client.post(
                path='{ep}/block/{id}'.format(
                    ep=eps.PERSONALITIES_ENDPOINT,
                    id=self.id,
                ),
                body=req_body,
            )

        if ports is not None:
            self._set_ports(ports)

        if hosts is not None:
            self._set_hosts(hosts)

        if host_groups is not None:
            self._set_host_groups(host_groups)

        self.load()
        self.clear_cache()

    def _set_host_groups(self, host_groups):
        # type: (List['HostGroup']) -> None

        desired_group_names = [group.name for group in host_groups]
        self_group_names = [group.name for group in self.host_groups]

        groups_to_remove = []
        groups_to_add = []

        for group_name in self_group_names:
            if group_name not in desired_group_names:
                groups_to_remove.append(
                    self._client.get_host_group(group_name).id
                )

        for group in host_groups:
            if group.name not in self_group_names:
                groups_to_add.append(group.id)

        for group_id in groups_to_remove:
            self._client.delete(
                path='{ep}/block/{resource_id}/groups/{group_id}'.format(
                    ep=eps.PERSONALITIES_ENDPOINT,
                    resource_id=self.id,
                    group_id=group_id,
                )
            )

        for group_id in groups_to_add:
            self._client.put(
                path='{ep}/block/{resource_id}/groups/{group_id}'.format(
                    ep=eps.PERSONALITIES_ENDPOINT,
                    resource_id=self.id,
                    group_id=group_id,
                )
            )

    def _set_hosts(self, hosts):
        # type: (List['Host']) -> None

        desired_host_names = [host.name for host in hosts]
        self_host_names = [host.name for host in self.hosts]

        hosts_to_remove = []
        hosts_to_add = []

        for host_name in self_host_names:
            if host_name not in desired_host_names:
                hosts_to_remove.append(
                    self._client.get_host(host_name).id
                )

        for host in hosts:
            if host.name not in self_host_names:
                hosts_to_add.append(host.id)

        for host_id in hosts_to_remove:
            self._client.delete(
                path='{ep}/block/{resource_id}/hosts/{host_id}'.format(
                    ep=eps.PERSONALITIES_ENDPOINT,
                    resource_id=self.id,
                    host_id=host_id,
                )
            )

        for host_id in hosts_to_add:
            self._client.put(
                path='{ep}/block/{resource_id}/hosts/{host_id}'.format(
                    ep=eps.PERSONALITIES_ENDPOINT,
                    resource_id=self.id,
                    host_id=host_id,
                )
            )

    def _set_ports(self, ports):
        # type: (List['Port']) -> None

        desired_port_names = [port.name for port in ports]
        self_port_names = [
            item['port'] for item in self._data.get('ports', [])
        ]

        ports_to_remove = []
        ports_to_add = []

        for port_name in self_port_names:
            if port_name not in desired_port_names:
                ports_to_remove.append(port_name)

        for port in ports:
            if port.name not in self_port_names:
                ports_to_add.append(port.name)

        for port_name in ports_to_remove:
            self._client.delete(
                path='{ep}/block/{resource_id}/ports/{port_id}'.format(
                    ep=eps.PERSONALITIES_ENDPOINT,
                    resource_id=self.id,
                    port_id=port_name,
                )
            )

        for port_id in ports_to_add:
            self._client.put(
                path='{ep}/block/{resource_id}/ports/{port_id}'.format(
                    ep=eps.PERSONALITIES_ENDPOINT,
                    resource_id=self.id,
                    port_id=port_id,
                )
            )

    def __eq__(self, other):
        if isinstance(other, ResourceBlock):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class ResourceFile(ResourceBase):

    @property
    def type(self):  # type: () -> str
        return self._data.get('type')

    @property
    def host_groups(self):  # type: () -> List
        return []

    @property
    def hosts(self):  # type: () -> List
        return []

    @property
    def subnets(self):  # type: () -> List['Subnet']
        rv = []

        all_subnets = self._cache.get('subnets')
        if all_subnets is None:
            all_subnets = self._cache['subnets'] = self._client.get_subnets()

        for subnet in all_subnets:
            if self in subnet.resources:
                rv.append(subnet)

        return rv

    @property
    def users(self):  # type: () -> List['User']
        rv = []

        all_users = self._cache.get('users')
        if all_users is None:
            all_users = self._cache['users'] = self._client.get_users()

        for item in self._data.get('acl', []):
            kind = item.get('principal', {}).get('kind')
            name = item.get('principal', {}).get('name')

            if kind == 'user':
                try:
                    user = next(u for u in all_users if u.name == name)
                except StopIteration:
                    raise TatlinClientError(
                        'Not found user {0} for resource {1}'.format(
                            name, self.name,
                        )
                    )

                rv.append(user)

        return rv

    @property
    def user_groups(self):
        # type: () -> List['UserGroup']

        rv = []

        all_groups = self._cache.get('user_groups')
        if all_groups is None:
            all_groups = self._cache['user_groups'] = \
                self._client.get_user_groups()

        for item in self._data.get('acl', []):
            kind = item.get('principal', {}).get('kind')
            name = item.get('principal', {}).get('name')

            if kind == 'group':
                try:
                    group = next(g for g in all_groups if g.name == name)
                except StopIteration:
                    raise TatlinClientError(
                        'Not found group {0} for resource {1}'.format(
                            name, self.name,
                        )
                    )

                rv.append(group)

        return rv

    def get_user_permissions(self, user):
        # type: ('User') -> str

        for item in self._data['acl']:
            if item['principal']['kind'] == 'user' \
                    and item['principal']['name'] == user.name:
                if {'read', 'write'} == set(item['permissions']):
                    return 'rw'
                elif ['read'] == item['permissions']:
                    return 'r'

                raise TatlinClientError(
                    'Unexpected permissions for user {0}'.format(
                        user.name,
                    )
                )

        raise TatlinClientError(
            'User {0} does not belong to resource {1}'.format(
                user.name, self.name,
            )
        )

    def get_user_group_permissions(self, group):
        # type: ('UserGroup') -> str

        for item in self._data['acl']:
            if item['principal']['kind'] == 'group' \
                    and item['principal']['name'] == group.name:
                if {'read', 'write'} == set(item['permissions']):
                    return 'rw'
                elif ['read'] == item['permissions']:
                    return 'r'

                raise TatlinClientError(
                    'Unexpected permissions for user group {0}'.format(
                        group.name,
                    )
                )

        raise TatlinClientError(
            'User group {0} does not belong to resource {1}'.format(
                group.name, self.name,
            )
        )

    def load(self):  # type: () -> None
        self._data = self._client.get('{ep}/file/{id}'.format(
            ep=eps.PERSONALITIES_ENDPOINT,
            id=self.id,
        )).json

    def update(
        self,
        read_cache=None,  # type: bool
        write_cache=None,  # type: bool
        ports=None,  # type: List['Port']
        subnets=None,  # type: List['Subnet']
        users=None,  # type: List[Tuple['User', str]]
        user_groups=None,  # type: List[Tuple['UserGroup', str]]
    ):  # type: (...) -> Task

        ports = ports if ports is not None else self.ports
        subnets = subnets if subnets is not None else self.subnets
        read_cache = read_cache if read_cache is not None else self.read_cache
        write_cache = write_cache \
            if write_cache is not None else self.write_cache

        acl = []

        if users is not None:
            self.validate_users(users)

            for user, permissions in users:
                acl.append({
                    'principal': {'kind': 'user', 'name': user.name},
                    'permissions': self.get_permissions_for_request(
                        permissions)
                })
        else:
            for item in self._data['acl']:
                if item['principal']['kind'] == 'user':
                    acl.append(item)

        if user_groups is not None:
            self.validate_user_groups(user_groups)

            for group, permissions in user_groups:
                acl.append({
                    'principal': {'kind': 'group', 'name': group.name},
                    'permissions': self.get_permissions_for_request(
                        permissions)
                })
        else:
            for item in self._data['acl']:
                if item['principal']['kind'] == 'group':
                    acl.append(item)

        task_data = self._client.put(
            path='{ep}/file/update/{id}'.format(
                ep=eps.DASHBOARD_RESOURCES_ENDPOINT,
                id=self.id,
            ),
            body={
                'id': self.id,
                'rCacheMode': 'enabled' if read_cache else 'disabled',
                'wCacheMode': 'enabled' if write_cache else 'disabled',
                'ports': [{'port': port.name} for port in ports],
                'subnets': [subnet.id for subnet in subnets],
                'acl': acl,
            },
        ).json

        self.load()
        self.clear_cache()

        return Task(client=self._client, **task_data)

    @staticmethod
    def get_permissions_for_request(permissions):
        # type: (str) -> List[str]
        if permissions == 'r':
            return ['read']
        elif permissions == 'rw':
            return ['read', 'write']

        raise TatlinClientError(
            'Unknown permissions: {0}'.format(permissions)
        )

    @staticmethod
    def validate_users(users):
        for user in users:
            if not any([
                isinstance(user, tuple),
                len(user) != 2,
                type(user[0]).__name__ != 'User',
                isinstance(user[1], str),
            ]):
                raise TatlinClientError(
                    'users argument must be a list of tuples '
                    'with two elements: (User, str)'
                )

    @staticmethod
    def validate_user_groups(groups):
        for group in groups:
            if not any([
                isinstance(group, tuple),
                len(group) != 2,
                type(group[0]).__name__ != 'UserGroup',
                isinstance(group[1], str),
            ]):
                raise TatlinClientError(
                    'user_groups argument must be a list of tuples '
                    'with two elements: (User, str)'
                )

    def __eq__(self, other):
        if isinstance(other, ResourceFile):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
