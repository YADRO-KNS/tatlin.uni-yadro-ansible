# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.osmgr.port import NodeAddress


@pytest.fixture
def ports_response():
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
                 "gateway": "***REMOVED***",
                 "nodes": {
                     "sp-0": [{"ipaddress": "***REMOVED***",
                               "netmask": "24",
                               "status": "online",
                               "ipaddressid": "mgmt0-ip-static-cfg-instance_attributes-ipaddress-1"
                               },
                              ],
                     "sp-1": [{"ipaddress": "***REMOVED***",
                               "netmask": "24",
                               "status": "online",
                               "ipaddressid": "mgmt1-ip-static-cfg-instance_attributes-ipaddress-2"
                               }]},
                 "failover": [{"ipaddress": "***REMOVED***",
                               "netmask": "24"}]}}
            ]


@pytest.fixture
def exp_addrs_sp0():
    return [NodeAddress(
        ip='***REMOVED***',
        mask='24',
        address_id='mgmt0-ip-static-cfg-instance_attributes-ipaddress-1',
        status='online',
    )]


@pytest.fixture
def exp_addrs_sp1():
    return [NodeAddress(
        ip='***REMOVED***',
        mask='24',
        address_id='mgmt1-ip-static-cfg-instance_attributes-ipaddress-2',
        status='online',
    )]
