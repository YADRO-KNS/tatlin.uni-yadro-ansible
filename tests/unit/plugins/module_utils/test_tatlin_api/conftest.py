# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import json
from ansible_collections.yadro.tatlin.tests.unit.compat.mock import MagicMock
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import OPEN_URL_FUNC
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.tatlin_client import TatlinClient


@pytest.fixture
def tatlin():
    return TatlinClient(
        base_url='localhost',
        username='admin',
        password='admin',
    )


@pytest.fixture
def make_mock(mocker):

    def f(target, return_value=None, side_effect=None, chain_calls=False):
        if return_value is None:
            return_value = {}

        if target == OPEN_URL_FUNC:
            return_value = _mock_open_url(return_value, chain_calls)

        mock = mocker.patch(
            target,
            side_effect=side_effect,
            return_value=return_value,
        )

        return mock

    def _mock_open_url(return_value, chain_calls):
        response_mock = MagicMock()
        if chain_calls and return_value is not None:
            gen = (json.dumps(d) for d in return_value)
            # Python 2 generators have next instead of __next__
            response_mock.read = gen.__next__ \
                if hasattr(gen, '__next__') else gen.next
        else:
            response_mock.read.return_value = json.dumps(return_value)
        return response_mock

    return f


@pytest.fixture
def open_url_kwargs():
    return {
        "method": 'GET',
        "url": "https://localhost",
        "data": None,
        "validate_certs": True,
        "use_proxy": True,
        "timeout": 60,
        "follow_redirects": "all",
        "headers": {},
        "force_basic_auth": False,
    }


# Sanity tests fail if there is unused import.
# This is the reason, why data fixtures are not in specific file
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
        "name": "test_block_resource1",
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
        "ports": [{
            "port": "p01",
            "port_status": "healthy",
            "port_status_desc": "resource is not available on all storage controllers",
            "wwn": [
                "iqn.2017-01.com.yadro:tatlin:sn.09092200c41002"
            ],
            "lun": "scsi-lun-p10-115",
            "volume": "pty-vol-4823db2c-75b8-4580-9cdd-95d8cfcc7da0",
            "lun_index": "115"}],
        "available_ports_number": 8,
        "volume_path": "/dev/mapper/dmc-fd968fd3-94fe-4896-b642-52bece3ca37b",
        "blockSize": "4kn",
        "replication": {
            "is_enabled": False
        },
        "ptyId": "c66dbc61-6e79-425b-b2ae-e396fd06ee68"
    },
        {
        "id": "48a75120-e8f9-42e7-8c42-2282047b4e3b",
        "name": "test_block_resource2",
        "type": "block",
        "poolId": "28118216-74eb-4ba2-8e01-be894b878de1",
        "volume_id": "pty-vol-48a75120-e8f9-42e7-8c42-2282047b4e3b",
        "size": 2097152,
        "maxModifySize": 135266304,
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
        "lbaFormat": "512e",
        "wwid": "naa.61452901325803104000800000000077",
        "lun_id": "119",
        "cached": "true",
        "rCacheMode": "disabled",
        "wCacheMode": "disabled",
        "alert_threshold": 70,
        "available_ports_number": 8,
        "volume_path": "/dev/mapper/dmc-a6ae8c22-790b-413e-927f-2baefe00ef59",
        "blockSize": "512e",
        "replication": {
            "is_enabled": False
        },
        "ptyId": "48a75120-e8f9-42e7-8c42-2282047b4e3b"
    },
        {
        "id": "4eae68d3-d793-4e08-972a-b64132e21f66",
        "name": "test_file_resource1",
        "type": "nfs",
        "poolId": "28118216-74eb-4ba2-8e01-be894b878de1",
        "volume_id": "blk-4eae68d3-d793-4e08-972a-b64132e21f66",
        "size": 104857600,
        "maxModifySize": 0,
        "status": "ready",
        "state": "running",
        "min_limit_iops": 10,
        "min_limit_bw": 10485760,
        "stat": {
            "used_capacity": 10485760,
            "mapped_blocks": 0,
            "dedup_count": 0,
            "reduction_ratio": 0
        },
        "cached": "true",
        "rCacheMode": "enabled",
        "wCacheMode": "enabled",
        "available_ports_number": 8,
        "ptyId": "4eae68d3-d793-4e08-972a-b64132e21f66"
    },
        {
        "id": "187ca049-e0cd-4cd8-ac85-0c478a1f915a",
        "name": "test_file_resource2",
        "type": "cifs",
        "poolId": "28118216-74eb-4ba2-8e01-be894b878de1",
        "volume_id": "blk-187ca049-e0cd-4cd8-ac85-0c478a1f915a",
        "size": 104857600,
        "maxModifySize": 0,
        "status": "ready",
        "state": "running",
        "min_limit_iops": 10,
        "min_limit_bw": 10485760,
        "stat": {
            "used_capacity": 5242880,
            "mapped_blocks": 0,
            "dedup_count": 0,
            "reduction_ratio": 0
        },
        "cached": "true",
        "rCacheMode": "disabled",
        "wCacheMode": "disabled",
        "available_ports_number": 8,
        "ptyId": "187ca049-e0cd-4cd8-ac85-0c478a1f915a"
    }]


@pytest.fixture
def ports_data():
    return [{"id": "p01",
             "meta": {
                 "type": "ip",
                 "data_role": False,
                 "replication_role": False},
             "params": {
                 "mtu": 1500,
                 "gateway": "",
                 "nodes": {"sp-0": [], "sp-1": []},
                 "failover": None}},
            {"id": "mgmt",
             "meta": {
                 "type": "ip",
                 "data_role": False,
                 "replication_role": False},
             "params": {
                 "mtu": 1500,
                 "gateway": "192.168.0.1",
                 "nodes": {
                     "sp-0": [{"ipaddress": "192.168.0.2",
                               "netmask": "24",
                               "status": "online",
                               "ipaddressid": "mgmt0-ip-static-cfg-instance_attributes-ipaddress-1"
                               },
                              ],
                     "sp-1": [{"ipaddress": "192.168.0.3",
                               "netmask": "24",
                               "status": "online",
                               "ipaddressid": "mgmt1-ip-static-cfg-instance_attributes-ipaddress-2"
                               }]},
                 "failover": [{"ipaddress": "192.168.0.4",
                               "netmask": "24"}]}},
            {"id": "p10",
             "meta": {
                 "type": "ip",
                 "data_role": False,
                 "replication_role": False},
             "params": {
                 "mtu": 1500,
                 "gateway": "",
                 "nodes": {"sp-0": [], "sp-1": []},
                 "failover": None}},
            ]


@pytest.fixture
def hosts_data():
    return [
        {
            "version": "cdf087471cd7d0cbb7b8b2ab019ebe88",
            "id": "7ab276b8-59a3-416b-8f28-191e91b4e20b",
            "name": "host1",
            "port_type": "iscsi",
            "initiators": [
                "iqn.1993-08.org.debian:01:5728e30474c"
            ],
            "tags": [
                "tag1",
                "tag2"
            ],
            "comment": "",
            "auth": {
                "internal_name": "hostname",
                "internal_password": "JLrGU-1qbCbb7XF1bFgEpkm2UatyH5H_EOrGIxs7BGE",
                "external_name": "targetname",
                "external_password": "Z5JJapsKhhkBwOIOfnHC34q0TCl2bmBjU_dnEeOECWo",
                "auth_type": "mutual"
            }
        },
        {
            "version": "41d0964c8d588d564a9122d888e6faa8",
            "id": "9355f65d-a8a2-4df9-8459-98a5c20725f3",
            "name": "host2",
            "port_type": "iscsi",
            "initiators": [],
            "tags": [
                "testtag"
            ],
            "comment": "",
            "auth": {
                "auth_type": "none"
            }
        },
    ]


@pytest.fixture
def host_groups_data():
    return [
        {
            "version": "6312695fd1834b46d3b38266a6042da2",
            "id": "02a41332-626f-40a7-a755-94650640477b",
            "name": "hostgroup1",
            "host_ids": [
                "7ab276b8-59a3-416b-8f28-191e91b4e20b",
                "9355f65d-a8a2-4df9-8459-98a5c20725f3",
            ],
            "tags": [
                "tag1",
                "tag2"
            ],
            "comment": ""
        },
        {
            "version": "e4b32e127683c87e14a194b6d33f04ba",
            "id": "a43aaf85-ad1d-4ac7-9433-09992c36a29a",
            "name": "hostgroup2",
            "host_ids": [],
            "tags": [],
            "comment": ""
        },
    ]


@pytest.fixture
def subnets_data():
    return [
        {"version": "2",
         "id": "1",
         "name": "subnet1",
         "comment": "",
         "tags": None,
         "resources": None,
         "ips": ["1.1.1.1", "2.2.2.2"]},
        {"version": "2",
         "id": "2",
         "name": "subnet2",
         "comment": "",
         "tags": None,
         "resources": None,
         "ips": ["8.8.8.8", "9.9.9.9"]}
    ]
