# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import check_obj
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import OPEN_URL_FUNC
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import (
    TATLIN_API_CLIENT_CLASS,
)


def get_drives_groups_response():
    return {
        "HDD_209715200": {
            "id": "HDD_209715200",
            "name": "HDD_209.71MB",
            "vendor": "YADRO",
            "model": "HDD_209715200",
            "totalDisks": 40,
            "usedDisks": 4,
            "availableDisks": 36,
            "failedDisks": 0,
            "warningDisks": 0,
            "failedCapacity": "0",
            "diskCapacity": "209715200",
            "diskType": "HDD",
            "totalCapacity": "8388608000",
            "usedCapacity": "838860800",
            "availableCapacity": "7549747200",
            "coldArchive": False,
            "disks": [{
                "id": "scsi-0YADRO_shared_disk_0450513bb2bbd68fdc7cb9f2e38d00c0",
                "model": "YADRO-shared_disk-2.5+",
                "vendor": "YADRO",
                "sn": "0450513bb2bbd68fdc7cb9f2e38d00c0",
                "type": "HDD",
                "system": False,
                "size": 209715200,
                "topology_path": "racks/0/diskbays/1000000001/disks/scsi-0YADRO_shared_disk_0450513bb2bbd68fdc7cb9f2e38d00c0",
                "state": "ok",
                "fw": "",
                "slot": "4"
            }]
        }
    }


def get_pools_response():
    return {
        "id": "28118216-74eb-4ba2-8e01-be894b878de1",
        "name": "testpool",
        "status": "ready",
        "media": {
            "model": "HDD_209715200",
            "coldArchive": False
        },
        "disks": "4",
        "disks_list": [
            "scsi-0YADRO_shared_disk_0450513bb2bbd68fdc7cb9f2e38d00c0",
        ],
        "capacity": "402653184",
        "spare": "1",
        "real_spare": "1",
        "max_spare": "1",
        "reserved_capacity": "201326592",
        "available": "33554432",
        "used": "369098752",
        "protection": "2+1",
        "failed": "0",
        "stripe_size": 8192,
        "thinProvision": False,
        "diskbays": [
            "1000000001"
        ],
        "resizing": False,
        "recovery": False,
        "health": "ok",
        "max_capacity": 4898947072,
        "max_disks_capacity": 40,
        "block_resource_max_size": 0,
        "file_resource_max_size": 0,
        "block_resource_limit": 5000000000000000,
        "file_resource_limit": 500000000000000,
        "resource_max_size": 0,
        "deduplication": False
    }


class TestDrives:

    def test_get_drive_group(self, tatlin, mock_method):
        # Mock open_url response with data
        mock_method(OPEN_URL_FUNC, **get_drives_groups_response())

        # Mock get_pools_method
        mock_method(
            TATLIN_API_CLIENT_CLASS + '.get_pools',
            get_pools_response(),
        )

        # Get drive group
        drive_group = tatlin.get_drive_groups()[0]

        # Result: Drive group with expected params was returned
        check_obj(drive_group, exp_params={
            'name': 'HDD_209.71MB',
            'type': 'HDD',
            'space_total': 8388608000,
            'space_available': 7549747200,
            'space_used': 838860800,
            'space_failed': 0,
            'drive_capacity': 209715200,
            'drives_total': 40,
            'drives_used': 4,
            'drives_available': 36,
            'drives_failed': 0,
            'drives_warning': 0,
        })

        assert drive_group.status == 'Ready', 'Drive group has wrong status'

        # Result: Group contains drive with expected params
        drive = drive_group.drives[0]
        check_obj(drive, exp_params={
            'id': 'scsi-0YADRO_shared_disk_0450513bb2bbd68fdc7cb9f2e38d00c0',
            'model': 'YADRO-shared_disk-2.5+',
            'serial_number': '0450513bb2bbd68fdc7cb9f2e38d00c0',
            'size': 209715200,
            'slot': '4',
            'pool': get_pools_response(),
        })

        assert drive.bay == '1000000001', 'Drive has wrong bay'
        assert drive.status == 'Healthy', 'Drive has wrong status'

    def test_warning_status(self, tatlin, mock_method):
        # Mock open_url response with data
        drive_groups_info = get_drives_groups_response()
        drive_groups_info['HDD_209715200']['warningDisks'] = 1
        drive_groups_info['HDD_209715200']['disks'][0]['state'] = 'warning'
        mock_method(OPEN_URL_FUNC, **drive_groups_info)

        # Mock get_pools_method
        mock_method(
            TATLIN_API_CLIENT_CLASS + '.get_pools',
            get_pools_response(),
        )

        # Get drive group
        drive_group = tatlin.get_drive_groups()[0]

        # Result: Drive group has status Warning
        assert drive_group.status == 'Warning', 'Drive group has wrong status'
        assert drive_group.drives[0].status == 'Warning', 'Drive has wrong status'

    def test_error_status(self, tatlin, mock_method):
        # Mock open_url response with data
        drive_groups_info = get_drives_groups_response()
        drive_groups_info['HDD_209715200']['failedDisks'] = 1
        drive_groups_info['HDD_209715200']['disks'][0]['state'] = 'error'
        mock_method(OPEN_URL_FUNC, **drive_groups_info)

        # Mock get_pools_method
        mock_method(
            TATLIN_API_CLIENT_CLASS + '.get_pools',
            get_pools_response(),
        )

        # Get drive group
        drive_group = tatlin.get_drive_groups()[0]

        # Result: Drive group has status Warning
        assert drive_group.status == 'Error', 'Drive group has wrong status'
        assert drive_group.drives[0].status == 'Error', 'Drive has wrong status'
