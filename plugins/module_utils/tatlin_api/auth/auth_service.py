# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    from typing import List, Optional, Union, Dict
except ImportError:
    # Satisfy Python 2 which doesn't have typing.
    List = Optional = Union = Dict = None

from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.auth.user import User
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.auth.group import UserGroup
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.auth.ldap_config import LdapConfig
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import (
    TatlinClientError,
    RESTClientNotFoundError
)


class AuthService:

    SERVICE_ENDPOINT = 'auth'
    USERS_ENDPOINT = SERVICE_ENDPOINT + '/' + 'users'
    GROUPS_ENDPOINT = SERVICE_ENDPOINT + '/' + 'groups'
    LDAP_ENDPOINT = SERVICE_ENDPOINT + '/' + 'ldap'
    LDAP_CONFIG_ENDOPINT = LDAP_ENDPOINT + '/' + 'configuration'

    def __init__(self, tatlin_client):
        self._client = tatlin_client
        self._ldap_config = None

    def create_group(self, name, parent_groups=None, comment=None):
        # type: (str, List[Union[str, UserGroup]], str) -> UserGroup

        member_of = []
        if parent_groups is not None:
            parent_groups = parent_groups \
                if isinstance(parent_groups, list) \
                else [parent_groups]

            for parent in parent_groups:
                member_of.append({
                    'Name': parent if isinstance(parent, str) else parent.name
                })

        self._client.put(
            self.GROUPS_ENDPOINT + '/' + name,
            body={
                'displayName': comment,
                'memberOf': member_of,
            }
        )

        group = self.get_group(name)
        if group is None:
            raise TatlinClientError(
                'Group {0} was not found after creation'.format(name)
            )

        return group

    def create_user(
        self,
        name,  # type: str
        password,  # type: str
        groups,  # type: List[Union[str, UserGroup]]
        enabled=True,  # type: Optional[bool]
    ):  # type: (...) -> User

        groups = groups if isinstance(groups, list) else [groups]
        member_of = []
        for group in groups:
            member_of.append(group if isinstance(group, str) else group.name)

        self._client.put(
            self.USERS_ENDPOINT + '/' + name,
            body={
                'secret': password,
                'memberOf': member_of,
                'enabled': 'true' if enabled else 'false',
            },
        )

        user = self.get_user(name)
        if user is None:
            raise TatlinClientError(
                'User {0} was not found after creation'.format(name)
            )

        return user

    def get_group(self, name):  # type: (str) -> Optional[UserGroup]
        try:
            data = self._client.get(self.GROUPS_ENDPOINT + '/' + name).json
        except RESTClientNotFoundError:
            return None

        # Tatlin returns dict with empty name if group is not exist
        # instead of 404. It is not correct, but we have to handle this
        if not data.get('name'):
            return None

        group = UserGroup(
            client=self._client,
            name=data['name'],
            gid=data['gid'],
            comment=data.get('displayName'),
        )
        return group

    def get_groups(self):  # type: () -> List[UserGroup]
        rv = []
        data = self._client.get(self.GROUPS_ENDPOINT).json

        for item in data:
            group = UserGroup(
                client=self._client,
                name=item['name'],
                gid=item['gid'],
                comment=item.get('displayName'),
            )
            rv.append(group)

        return rv

    def get_user(self, name):  # type: (str) -> Optional[User]
        try:
            data = self._client.get(self.USERS_ENDPOINT + '/' + name).json
        except RESTClientNotFoundError:
            return None

        user = User(
            client=self._client,
            name=data['name'],
            uid=data['uid'],
            enabled=data['enabled'],
            member_of=data['memberOf'],
        )

        return user

    def get_users(self):  # type: () -> List[User]
        rv = []
        data = self._client.get(self.USERS_ENDPOINT).json
        for item in data.values():
            user = User(
                client=self._client,
                name=item['name'],
                uid=item['uid'],
                enabled=item['enabled'],
                member_of=item['memberOf'],
            )
            rv.append(user)
        return rv

    def get_ldap_config(self):  # type: () -> LdapConfig
        if self._ldap_config is None:
            self._ldap_config = LdapConfig(self._client)
        self._ldap_config.load()
        return self._ldap_config
