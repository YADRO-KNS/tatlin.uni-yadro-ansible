# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest


@pytest.fixture
def drives_groups_data():
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


@pytest.fixture
def pools_data():
    return [{
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
    }]


@pytest.fixture
def resources_data():
    return [{
        "id": "c66dbc61-6e79-425b-b2ae-e396fd06ee68",
        "name": "rsrc",
        "type": "block",
        "poolId": "28118216-74eb-4ba2-8e01-be894b878de1",
        "volume_id": "pty-vol-c66dbc61-6e79-425b-b2ae-e396fd06ee68",
        "size": 1048576,
        "maxModifySize": 353370112,
        "status": "ready",
        "min_limit_iops": 10,
        "min_limit_bw": 10485760,
        "overhead": 15728640,
        "stat": {
            "used_capacity": 1048576,
            "mapped_blocks": 0,
            "dedup_count": 0,
            "reduction_ratio": 0
        },
        "lbaFormat": "4kn",
        "wwid": "naa.61452901305803104000800000000001",
        "lun_id": "1",
        "cached": "true",
        "rCacheMode": "enabled",
        "wCacheMode": "enabled",
        "available_ports_number": 8,
        "volume_path": "/dev/mapper/dmc-fd968fd3-94fe-4896-b642-52bece3ca37b",
        "blockSize": "4kn",
        "replication": {
            "is_enabled": False
        },
        "ptyId": "c66dbc61-6e79-425b-b2ae-e396fd06ee68"
    }]
