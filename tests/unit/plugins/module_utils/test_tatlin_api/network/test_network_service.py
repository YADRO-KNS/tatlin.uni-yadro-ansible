# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.network.port import Node
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import OPEN_URL_FUNC
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import check_object


def get_ports_response():
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
                               "netmask": "24"}],
                     "sp-1": [{"ipaddress": "***REMOVED***",
                               "netmask": "24"}]},
                 "failover": [{"ipaddress": "***REMOVED***",
                               "netmask": "24"}]}}
            ]


class TestNetworkService:

    def test_get_ports(self, client, mock_method):
        # Mock open_url response for get_ports
        mock_method(
            OPEN_URL_FUNC,
            *get_ports_response()
        )

        # Call get_ports
        ports = client.network_service.get_ports()

        # Result: two ports was returned
        assert len(ports) == 2

        # Define expected ports
        mgmt_port = next(port for port in ports if port.name == 'mgmt')
        p01_port = next(port for port in ports if port.name == 'p01')
        expected_ports = [
            {'name': 'p01',
             'type': 'ip',
             'gateway': '',
             'mtu': 1500,
             'nodes': {"sp-0": Node(client, p01_port, 'sp-0', []),
                       "sp-1": Node(client, p01_port, 'sp-1', [])},
             'virtual_address': ''},
            {'name': 'mgmt',
             'type': 'ip',
             'gateway': '***REMOVED***',
             'mtu': 1500,
             'nodes': {
                 "sp-0": Node(client, mgmt_port, 'sp-0', ['***REMOVED***/24']),
                 "sp-1": Node(client, mgmt_port, 'sp-1', ['***REMOVED***/24'])},
             'virtual_address': '***REMOVED***/24'}
        ]

        # Result: Ports with expected params was returned
        for port in ports:
            check_object(port, expected_ports)

        # Additional check, because addresses actually don't
        # checked at the above checking
        # Result: Nodes with expected params was returned
        check_object(
            mgmt_port.nodes['sp-0'],
            dict(name='sp-0', addresses=['***REMOVED***/24']),
        )
        check_object(
            mgmt_port.nodes['sp-1'],
            dict(name='sp-1', addresses=['***REMOVED***/24']),
        )
        check_object(
            p01_port.nodes['sp-0'],
            dict(name='sp-0', addresses=[]),
        )
        check_object(
            p01_port.nodes['sp-1'],
            dict(name='sp-1', addresses=[]),
        )

    def test_get_port(self, client, mock_method):
        # Mock open_url response for get_ports
        mock_method(
            OPEN_URL_FUNC,
            *get_ports_response()
        )

        # Call get_port
        mgmt_port = client.network_service.get_port('mgmt')

        # Define expected port
        expected_ports = [
            {'name': 'mgmt',
             'type': 'ip',
             'gateway': '***REMOVED***',
             'mtu': 1500,
             'nodes': {
                 "sp-0": Node(client, mgmt_port, 'sp-0', ['***REMOVED***/24']),
                 "sp-1": Node(client, mgmt_port, 'sp-1', ['***REMOVED***/24'])},
             'virtual_address': '***REMOVED***/24'}
        ]

        # Result: Port with expected params was returned
        check_object(mgmt_port, expected_ports)

        # Additional check, because addresses actually don't
        # checked at the above checking
        # Result: Nodes with expected params was returned
        check_object(
            mgmt_port.nodes['sp-0'],
            dict(name='sp-0', addresses=['***REMOVED***/24']),
        )
        check_object(
            mgmt_port.nodes['sp-1'],
            dict(name='sp-1', addresses=['***REMOVED***/24']),
        )

    def test_get_non_existing_port(self, client, mock_method):
        # Mock open_url response for get_ports
        mock_method(
            OPEN_URL_FUNC,
            *get_ports_response()
        )

        # Call get_port
        with pytest.raises(TatlinClientError) as exc_info:
            client.network_service.get_port('AbsentPort')

        assert str(exc_info.value) == 'Not found port with name AbsentPort'

    def test_get_ntp_config(self, client, mock_method):
        # Mock open_url response for get_ports
        mock_method(
            OPEN_URL_FUNC,
            ntp_server_list=['127.0.0.1']
        )

        # Call get_ntp_config
        ntp_config = client.network_service.get_ntp_config()

        # Result: Config with expected server was returned
        assert ntp_config.servers == ['127.0.0.1']
