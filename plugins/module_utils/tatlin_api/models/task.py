# -*- coding: utf-8 -*-

# YADRO Tatlin Unified Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import time
import ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.endpoints as eps
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.exception import TatlinTaskError


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

    def wait_until_complete(self, timeout=120):  # type: (int) -> None
        start_time = time.time()
        while self.state != 'done':
            if time.time() - start_time > timeout:
                raise TimeoutError(
                    'Task has not done state for {0} seconds'.format(timeout),
                )

            time.sleep(0.1)
            self.load()

            if self.state in ('error', 'aborting', 'aborted'):
                if self.state == 'error':
                    msg = 'Tatlin task {0} was finished ' \
                          'with error state'.format(self.id)
                else:
                    msg = self.err_msg
                raise TatlinTaskError(msg)

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
