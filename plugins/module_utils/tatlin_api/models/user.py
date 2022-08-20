# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    from typing import Union, List, TYPE_CHECKING
except ImportError:
    Union = List = TYPE_CHECKING = None

from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import USERS_ENDPOINT

if TYPE_CHECKING:
    from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.models.user_group import UserGroup


class User:

    def __init__(self, client, name, uid, enabled, member_of):
        self._client = client
        self.name = name
        self.uid = uid
        self.enabled = enabled
        self._member_of = member_of
        self._endpoint = '/'.join([USERS_ENDPOINT, self.name])

    def delete(self):  # type: () -> None
        self._client.delete(self._endpoint)

    def update(self, password=None, enabled=None, groups=None):
        # type: (str, bool, List[Union[str, 'UserGroup']]) -> None
        """
        Note:
             Updating groups will replace all user's groups by
             values at the argument
        """

        upd_params = {}

        if enabled is not None:
            upd_params['enabled'] = 'true' if enabled else 'false'

        if password is not None:
            upd_params['secret'] = password

        if groups is not None:
            member_of = []
            for group in groups:
                member_of.append(
                    group if isinstance(group, str) else group.name
                )
            upd_params['memberOf'] = member_of

        if len(upd_params) == 0:
            raise TypeError(
                'At least one argument must be passed for user update'
            )

        self._client.post(self._endpoint, body=upd_params)
        self.reload()

    def reload(self):  # type: () -> None
        data = self._client.get(self._endpoint).json
        self.enabled = data['enabled']
        self._member_of = data['memberOf']

    @property
    def groups(self):
        user_groups = []
        self.reload()

        all_groups = self._client.get_user_groups()
        for group in all_groups:
            if group.name in self._member_of:
                user_groups.append(group)

        return user_groups

    def __eq__(self, other):
        if isinstance(other, User):
            return self.uid == other.uid
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
