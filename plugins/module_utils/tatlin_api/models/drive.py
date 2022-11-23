# -*- coding: utf-8 -*-

# YADRO Tatlin Unified Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    from typing import List, Dict, Optional
except ImportError:
    List = Dict = Optional = None


class DRIVE_STATUS:
    WARNING = 'Warning'
    ERROR = 'Error'
    HEALTHY = 'Healthy'


class Drive:

    def __init__(self, client, drive_group, pool, **drive_data):
        self._client = client
        self._state = drive_data['state']
        self._topology_path = drive_data['topology_path']
        self._bay = None

        self.drive_group = drive_group
        self.id = drive_data['id']
        self.model = drive_data['model']
        self.serial_number = drive_data['sn']
        self.size = drive_data['size']
        self.slot = drive_data['slot']
        self.pool = pool

    @property
    def bay(self):  # type: () -> str
        if self._bay is None:
            topology_parts = self._topology_path.split('/')
            self._bay = topology_parts[-3] \
                if len(topology_parts) > 3 else topology_parts
        return self._bay

    @property
    def status(self):  # type: () -> str
        if self._state.lower() == 'error':
            return DRIVE_STATUS.ERROR
        if self._state.lower() == 'warning':
            return DRIVE_STATUS.WARNING
        return DRIVE_STATUS.HEALTHY

    def __eq__(self, other):
        if isinstance(other, Drive):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
