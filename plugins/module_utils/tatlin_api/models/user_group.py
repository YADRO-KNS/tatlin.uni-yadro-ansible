# -*- coding: utf-8 -*-

# YADRO Tatlin Unified Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    from typing import Optional, Union, List
except ImportError:
    Optional = Union = List = None

from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.models.user import User
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.endpoints import GROUPS_ENDPOINT


class UserGroup:

    def __init__(self, client, name, gid, member_of=None, comment=None):
        self._client = client
        self.name = name
        self.gid = gid
        self.comment = comment or ''
        self._member_of = member_of or []
        self._endpoint = '/'.join([GROUPS_ENDPOINT, self.name])

    def delete(self):  # type: () -> None
        self._client.delete(self._endpoint)

    def update(self, comment=None, parent_groups=None):
        # type: (str, List[Union[str, User]]) -> None

        if comment is None and parent_groups is None:
            raise TypeError(
                'At least one argument must be passed for group update'
            )

        upd_params = {}

        if comment is not None:
            upd_params['displayName'] = comment
        else:
            upd_params['displayName'] = self.comment

        if parent_groups is not None:
            upd_params['memberOf'] = []
            parent_groups = parent_groups \
                if isinstance(parent_groups, list) \
                else [parent_groups]

            for parent in parent_groups:
                upd_params['memberOf'].append({
                    'Name': parent if isinstance(parent, str) else parent.name
                })
        else:
            upd_params['memberOf'] = self._member_of

        self._client.post(self._endpoint, body=upd_params)
        self.reload()

    def reload(self):  # type: () -> None
        data = self._client.get(self._endpoint).json
        self.comment = data.get('displayName', '')
        self._member_of = data.get('memberOf', [])

    @property
    def users(self):  # type: () -> List[User]
        rv = []

        data = self._client.get(self._endpoint + '/users').json
        for d in data.values():
            user = User(
                client=self._client,
                name=d['name'],
                uid=d['uid'],
                enabled=d['enabled'],
                member_of=d['memberOf'],
            )

            rv.append(user)

        return rv

    @property
    def parent_groups(self):  # type: () -> List[UserGroup]
        rv = []
        self.reload()

        parent_names = set(g['name'] for g in self._member_of)

        all_groups = self._client.get_user_groups()
        for group in all_groups:
            if group.name in parent_names:
                rv.append(group)

        return rv

    def __eq__(self, other):
        if isinstance(other, UserGroup):
            return self.gid == other.gid
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
