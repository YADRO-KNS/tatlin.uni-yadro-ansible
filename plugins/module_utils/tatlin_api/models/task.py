# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints as eps


class Task:

    def __init__(self, client, **data):
        self._client = client
        self._data = data

    @property
    def id(self):  # type: () -> int
        rv = self._data.get('id')
        if rv is None:
            raise AttributeError(
                'Task object has no id value'
            )
        return rv

    @property
    def err_msg(self):  # type: () -> str
        return self._data.get('err_msg')

    @property
    def state(self):  # type: () -> str
        return self._data.get('state')

    def load(self):
        self._data = self._client.get('{0}/{1}'.format(
            eps.DASHBOARD_TASKS_ENDPOINT, self.id
        )).json

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
