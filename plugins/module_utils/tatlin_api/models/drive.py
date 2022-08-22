# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    from typing import List, Dict, Optional
except ImportError:
    List = Dict = Optional = None


class DRIVE_GROUP_STATUS:
    WARNING = 'Warning'
    ERROR = 'Error'
    READY = 'Ready'


class DRIVE_STATUS:
    WARNING = 'Warning'
    ERROR = 'Error'
    HEALTHY = 'Healthy'


class DriveGroup:

    def __init__(self, client, **drive_group_data):
        self._client = client
        self.name = drive_group_data['name']
        self.type = drive_group_data['diskType']
        self.space_total = int(drive_group_data['totalCapacity'])
        self.space_available = int(drive_group_data['availableCapacity'])
        self.space_used = int(drive_group_data['usedCapacity'])
        self.space_failed = int(drive_group_data['failedCapacity'])
        self.drive_capacity = int(drive_group_data['diskCapacity'])
        self.drives_total = drive_group_data['totalDisks']
        self.drives_used = drive_group_data['usedDisks']
        self.drives_available = drive_group_data['availableDisks']
        self.drives_failed = drive_group_data['failedDisks']
        self.drives_warning = drive_group_data['warningDisks']

        self.drives = []
        pools = drive_group_data.get('pools', self._client.get_pools()) or []
        for drive_info in drive_group_data.get('disks', []):
            drive_info['pool'] = self._get_pool_for_drive(drive_info, pools)
            self.drives.append(
                Drive(client=self._client, **drive_info)
            )

    @property
    def status(self):  # type: () -> str
        if self.drives_failed > 0:
            return DRIVE_GROUP_STATUS.ERROR
        if self.drives_warning > 0:
            return DRIVE_GROUP_STATUS.WARNING
        return DRIVE_GROUP_STATUS.READY

    @staticmethod
    def _get_pool_for_drive(drive_info, pools):
        # type: (Dict, List[Dict]) -> Optional[Dict]
        drive_id = drive_info['id']
        for pool in pools:
            if drive_id in pool['disks_list']:
                return pool
        return None


class Drive:

    def __init__(self, client, **drive_info):
        self._client = client
        self._state = drive_info['state']
        self._topology_path = drive_info['topology_path']
        self._bay = None

        self.id = drive_info['id']
        self.model = drive_info['model']
        self.serial_number = drive_info['sn']
        self.size = drive_info['size']
        self.slot = drive_info['slot']
        self.pool = drive_info.get('pool')

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
            return self.serial_number == other.serial_number
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
