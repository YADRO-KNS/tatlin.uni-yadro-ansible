# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.osmgr.port import Node, VirtualAddress
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import (
    TatlinClientError, TatlinNodeNotFoundError, RESTClientNotFoundError)
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import REBOOT_ENDPOINT
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import OPEN_URL_FUNC
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import check_obj


class TestNetworkService:

    def test_get_ports(
        self, client, mock_method, ports_response, exp_addrs_sp0, exp_addrs_sp1,
    ):
        # Mock open_url response for get_ports
        mock_method(
            OPEN_URL_FUNC,
            *ports_response
        )

        # Call get_ports
        ports = client.osmgr_service.get_ports()

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
             'virtual_address': None},
            {'name': 'mgmt',
             'type': 'ip',
             'gateway': '***REMOVED***',
             'mtu': 1500,
             'nodes': {
                 "sp-0": Node(client, mgmt_port, 'sp-0', exp_addrs_sp0),
                 "sp-1": Node(client, mgmt_port, 'sp-1', exp_addrs_sp1),
             },
             'virtual_address': VirtualAddress(ip='***REMOVED***', mask='24')}
        ]

        # Result: Ports with expected params was returned
        for port in ports:
            check_obj(port, expected_ports)

        # Additional check, because addresses actually don't
        # checked at the above checking
        # Result: Nodes with expected params was returned
        check_obj(
            mgmt_port.nodes['sp-0'],
            dict(name='sp-0', addresses=exp_addrs_sp0),
        )
        check_obj(
            mgmt_port.nodes['sp-1'],
            dict(name='sp-1', addresses=exp_addrs_sp1),
        )
        check_obj(
            p01_port.nodes['sp-0'],
            dict(name='sp-0', addresses=[]),
        )
        check_obj(
            p01_port.nodes['sp-1'],
            dict(name='sp-1', addresses=[]),
        )

    def test_get_port(
        self, client, mock_method, ports_response, exp_addrs_sp0, exp_addrs_sp1,
    ):
        # Mock open_url response for get_ports
        mock_method(
            OPEN_URL_FUNC,
            *ports_response
        )

        # Call get_port
        mgmt_port = client.osmgr_service.get_port('mgmt')

        expected_ports = [
            {'name': 'mgmt',
             'type': 'ip',
             'gateway': '***REMOVED***',
             'mtu': 1500,
             'nodes': {
                 "sp-0": Node(client, mgmt_port, 'sp-0', exp_addrs_sp0),
                 "sp-1": Node(client, mgmt_port, 'sp-1', exp_addrs_sp1)},
             'virtual_address': VirtualAddress(ip='***REMOVED***', mask='24')}
        ]

        # Result: Port with expected params was returned
        check_obj(mgmt_port, expected_ports)

        # Additional check, because addresses actually don't
        # checked at the above checking
        # Result: Nodes with expected params was returned
        check_obj(
            mgmt_port.nodes['sp-0'],
            dict(name='sp-0', addresses=exp_addrs_sp0),
        )
        check_obj(
            mgmt_port.nodes['sp-1'],
            dict(name='sp-1', addresses=exp_addrs_sp1),
        )

    def test_get_non_existing_port(self, client, mock_method, ports_response):
        # Mock open_url response for get_ports
        mock_method(
            OPEN_URL_FUNC,
            *ports_response
        )

        # Call get_port
        with pytest.raises(TatlinClientError) as exc_info:
            client.osmgr_service.get_port('AbsentPort')

        assert str(exc_info.value) == 'Not found port with name AbsentPort'

    def test_get_ntp_config(self, client, mock_method):
        # Mock open_url response for get_ports
        mock_method(
            OPEN_URL_FUNC,
            ntp_server_list=['127.0.0.1']
        )

        # Call get_ntp_config
        ntp_config = client.osmgr_service.get_ntp_config()

        # Result: Config with expected server was returned
        assert ntp_config.servers == ['127.0.0.1']

    def test_get_dns_filled_config(self, client, mock_method):
        # Mock open_url response with data
        mock_method(
            OPEN_URL_FUNC,
            dns_static_servers=['127.0.0.1', '1.1.1.1'],
            dns_static_search_list=['exapmle.com', 'test.com']
        )

        # Get DNS config
        dns_config = client.osmgr_service.get_dns_config()

        # Result: DNS config with expected parameters was returned
        assert dns_config.servers == ['127.0.0.1', '1.1.1.1']
        assert dns_config.search_list == ['exapmle.com', 'test.com']

    def test_get_dns_empty_config(self, client, mock_method):
        # Mock open_url response with data
        mock_method(
            OPEN_URL_FUNC,
            dns_static_servers=[],
            dns_static_search_list=[]
        )

        # Get DNS config
        dns_config = client.osmgr_service.get_dns_config()

        # Result: DNS config with expected parameters was returned
        assert dns_config.servers == []
        assert dns_config.search_list == []

    @pytest.mark.parametrize(
        'node_name', ['sp-0', 'sp-1']
    )
    def test_reboot_node(self, client, mock_method, open_url_kwargs, node_name):
        # Mock open_url without data
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Reboot node
        client.osmgr_service.reboot_node(node_name)

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(
                REBOOT_ENDPOINT.format(node=node_name)
            ),
        )

        # Result: open_url was called with expected parameters
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_reboot_non_existing_node(self, client, mock_method, open_url_kwargs):
        # Mock open_url with not found error
        mock_method(target=OPEN_URL_FUNC, side_effects=RESTClientNotFoundError)

        # Reboot non-existing node
        # Result: TatlinNodeNotFoundError was raised
        with pytest.raises(TatlinNodeNotFoundError):
            client.osmgr_service.reboot_node('test-node')
