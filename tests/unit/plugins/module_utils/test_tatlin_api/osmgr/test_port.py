# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import pytest
from hamcrest import assert_that, has_entries
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import check_obj
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import (
    OPEN_URL_FUNC, PORT_CLASS, PORT_MODULE,
)
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import PORTS_ENDPOINT, PORTS_STATUS_ENDPOINT
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.osmgr.port import (
    get_ip_and_mask, get_ip, Port, Node, NodeAddress, VirtualAddress, ChangedHost,
)
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import (
    RESTClientConnectionError, TatlinClientError,
)


def get_addrs_for_request(*addresses):
    rv = []

    for addr in addresses:
        ip = mask = None
        if addr:
            ip, mask = addr.ip, addr.mask
        rv.append({'ipaddress': ip, 'netmask': mask})

    return rv


class TestPort:

    def test_get_ip_and_mask(self):
        ip, mask = get_ip_and_mask('192.168.0.31/30')
        assert ip == '192.168.0.31'
        assert mask == '30'

    def test_get_ip_one_address_str(self):
        ip = get_ip('192.168.0.31/30')
        assert type(ip) == str
        assert ip == '192.168.0.31'

    def test_get_ip_one_address_list(self):
        ip = get_ip(['192.168.0.31/30'])
        assert type(ip) == list
        assert ip == ['192.168.0.31']

    def test_get_ip_two_addresses(self):
        ip = get_ip(['192.168.0.31/30', '192.168.20.100/30'])
        assert ip == ['192.168.0.31', '192.168.20.100']

    def test_changed_host(self, client):
        # Create context manager
        changed_host = ChangedHost(client=client)

        # Ensure that we use specific host
        assert client.get_host() == 'localhost'

        # Change client's host
        with changed_host('new_host'):
            assert client.get_host() == 'new_host'

        # Result: init host is used after context manager
        assert client.get_host() == 'localhost'

    def test_port_is_mgmt_true(self, client, mock_method, ports_response):
        # Create mgmt port
        port = Port(client=client, port_data=ports_response[1])

        # Get port mgmt status
        is_mgmt = port.is_mgmt()

        # Result: port is mgmt
        assert is_mgmt is True

    def test_port_is_mgmt_false(self, client, mock_method, ports_response):
        # Create data port
        port = Port(client=client, port_data=ports_response[0])

        # Get port mgmt status
        is_mgmt = port.is_mgmt()

        # Result: port is not mgmt
        assert is_mgmt is False

    def test_port_load_with_addresses(
        self, client, mock_method, ports_response,
        exp_addrs_sp0, exp_addrs_sp1,
    ):
        # Create port with empty data
        port = Port(client=client, port_data={
            "id": "mgmt",
            "meta": {"type": "ip"},
            "params": {
                "mtu": None,
                "gateway": None,
                "nodes": {
                    "sp-0": [],
                    "sp-1": []},
                "failover": []}
        })

        # Ensure that port has empty attributes
        check_obj(
            port, dict(
                gateway=None,
                mtu=None,
                nodes={'sp-0': Node(client, port, 'sp-0', []),
                       'sp-1': Node(client, port, 'sp-1', [])},
                virtual_address=None
            ),
        )

        # Mock open_url with data
        mock_method(OPEN_URL_FUNC, **ports_response[1])

        # Load port
        port.load()

        # Define expected port
        expected_port = {
            'name': 'mgmt',
            'type': 'ip',
            'gateway': '***REMOVED***',
            'mtu': 1500,
            'nodes': {
                "sp-0": Node(client, port, 'sp-0', exp_addrs_sp0),
                "sp-1": Node(client, port, 'sp-1', exp_addrs_sp1)},
            'virtual_address': VirtualAddress(ip='***REMOVED***', mask='24'),
        }

        # Result: Port has expected attributes
        check_obj(port, expected_port)

        # Additional check, because addresses actually don't
        # checked at the above checking
        # Result: Nodes with expected params was returned
        check_obj(
            port.nodes['sp-0'],
            dict(name='sp-0', addresses=exp_addrs_sp0),
        )
        check_obj(
            port.nodes['sp-1'],
            dict(name='sp-1', addresses=exp_addrs_sp1),
        )

    def test_port_load_wo_addresses(
        self, client, mock_method, ports_response
    ):
        # Create port with empty data
        port = Port(client=client, port_data={
            "id": "p01",
            "meta": {"type": "ip"},
            "params": {
                "mtu": None,
                "gateway": None,
                "nodes": {
                    "sp-0": [],
                    "sp-1": []},
                "failover": []}
        })

        # Ensure that port has empty attributes
        check_obj(
            port, dict(
                gateway=None,
                mtu=None,
                nodes={'sp-0': Node(client, port, 'sp-0', []),
                       'sp-1': Node(client, port, 'sp-1', [])},
                virtual_address=None
            ),
        )

        # Mock open_url with data
        mock_method(OPEN_URL_FUNC, **ports_response[0])

        # Load port
        port.load()

        # Define expected port
        expected_port = {
            'name': 'p01',
            'type': 'ip',
            'gateway': '',
            'mtu': 1500,
            'nodes': {"sp-0": Node(client, port, 'sp-0', []),
                      "sp-1": Node(client, port, 'sp-1', [])},
            'virtual_address': None
        }

        # Result: Port has expected attributes
        check_obj(port, expected_port)

        # Additional check, because addresses actually don't
        # checked at the above checking
        # Result: Nodes with expected params was returned
        check_obj(
            port.nodes['sp-0'],
            dict(name='sp-0', addresses=[]),
        )
        check_obj(
            port.nodes['sp-1'],
            dict(name='sp-1', addresses=[]),
        )

    @pytest.mark.parametrize('port_name', ['mgmt', 'p01'])
    def test_update_mtu(
        self, client, mock_method, open_url_kwargs,
        port_name, mocker, ports_response,
    ):
        # Create port object
        port_data = next(data for data in ports_response
                         if data['id'] == port_name)

        port = Port(client=client, port_data=port_data)

        # Mock load method without data
        mock_method(PORT_CLASS + '.load')

        # Mock open_url method
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Defining expected call parameters
        open_url_kwargs.update(
            method='POST',
            url='https://localhost/{0}/{1}/{2}'.format(
                PORTS_ENDPOINT,
                port.type,
                port.name),
            data=mocker.ANY,
            headers={'Content-Type': 'application/json'},
        )

        # Change port mtu
        port.update(mtu=1501)

        # Result: Request with expected parameters was sent to tatlin
        open_url_mock.assert_called_with(**open_url_kwargs)

        # Satisfy Python <= 2.7 & 3.5. It does not have builtin dict order,
        # so resulting json may be in different order than expected
        call_args, call_kwargs = open_url_mock.call_args
        call_data = json.loads(call_kwargs['data'])

        expected_call_data = {
            'params': {
                'nodes': {
                    'sp-0': get_addrs_for_request(
                        *port.nodes['sp-0'].addresses),
                    'sp-1': get_addrs_for_request(
                        *port.nodes['sp-1'].addresses),
                },
                'failover': get_addrs_for_request(port.virtual_address),
                'gateway': port.gateway,
                'mtu': 1501,
            },
        }
        assert_that(call_data, has_entries(expected_call_data))

    @pytest.mark.parametrize('port_name', ['mgmt', 'p01'])
    def test_update_gateway(
        self, client, mock_method, open_url_kwargs,
        port_name, mocker, ports_response,
    ):
        # Create port object
        port_data = next(data for data in ports_response
                         if data['id'] == port_name)

        port = Port(client=client, port_data=port_data)

        # Mock load method without data
        mock_method(PORT_CLASS + '.load')

        # Mock open_url method
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Defining expected call parameters
        open_url_kwargs.update(
            method='POST',
            url='https://localhost/{0}/{1}/{2}'.format(
                PORTS_ENDPOINT,
                port.type,
                port.name),
            data=mocker.ANY,
            headers={'Content-Type': 'application/json'},
        )

        # Change port mtu
        port.update(gateway='192.168.111.1')

        # Result: Request with expected parameters was sent to tatlin
        open_url_mock.assert_called_with(**open_url_kwargs)

        # Satisfy Python <= 2.7 & 3.5. It does not have builtin dict order,
        # so resulting json may be in different order than expected
        call_args, call_kwargs = open_url_mock.call_args
        call_data = json.loads(call_kwargs['data'])
        expected_call_data = {
            'params': {
                'nodes': {
                    'sp-0': get_addrs_for_request(
                        *port.nodes['sp-0'].addresses),
                    'sp-1': get_addrs_for_request(
                        *port.nodes['sp-1'].addresses),
                },
                'failover': get_addrs_for_request(port.virtual_address),
                'gateway': '192.168.111.1',
                'mtu': port.mtu,
            },
        }
        assert_that(call_data, has_entries(expected_call_data))

    @pytest.mark.parametrize('port_name', ['mgmt', 'p01'])
    def test_update_virtual_address(
        self, client, mock_method, open_url_kwargs,
        port_name, mocker, ports_response,
    ):
        # Create port object
        port_data = next(data for data in ports_response
                         if data['id'] == port_name)

        port = Port(client=client, port_data=port_data)

        # Mock load method without data
        mock_method(PORT_CLASS + '.load')

        # Mock open_url method
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Mock waiting interfaces method
        mock_method(target=PORT_CLASS + '._wait_interfaces_up')

        # Defining expected call parameters
        open_url_kwargs.update(
            method='POST',
            url='https://localhost/{0}/{1}/{2}'.format(
                PORTS_ENDPOINT,
                port.type,
                port.name),
            data=mocker.ANY,
            headers={'Content-Type': 'application/json'},
        )

        # Change port mtu
        port.update(virtual_address='192.168.1.111/24')

        # Result: Request with expected parameters was sent to tatlin
        open_url_mock.assert_called_with(**open_url_kwargs)

        # Satisfy Python <= 2.7 & 3.5. It does not have builtin dict order,
        # so resulting json may be in different order than expected
        call_args, call_kwargs = open_url_mock.call_args
        call_data = json.loads(call_kwargs['data'])
        expected_call_data = {
            'params': {
                'nodes': {
                    'sp-0': get_addrs_for_request(
                        *port.nodes['sp-0'].addresses),
                    'sp-1': get_addrs_for_request(
                        *port.nodes['sp-1'].addresses),
                },
                'failover': get_addrs_for_request(VirtualAddress(ip='192.168.1.111', mask='24')),
                'gateway': port.gateway,
                'mtu': port.mtu,
            },
        }
        assert_that(call_data, has_entries(expected_call_data))

    @pytest.mark.parametrize('port_name', ['mgmt', 'p01'])
    def test_update_sp_addresses(
        self, client, mock_method, open_url_kwargs,
        port_name, mocker, ports_response,
    ):
        # Create port object
        port_data = next(data for data in ports_response
                         if data['id'] == port_name)

        port = Port(client=client, port_data=port_data)

        # Mock load method without data
        mock_method(PORT_CLASS + '.load')

        # Mock open_url method
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Mock waiting interfaces method
        mock_method(target=PORT_CLASS + '._wait_interfaces_up')

        # Defining expected call parameters
        open_url_kwargs.update(
            method='POST',
            url='https://localhost/{0}/{1}/{2}'.format(
                PORTS_ENDPOINT,
                port.type,
                port.name),
            data=mocker.ANY,
            headers={'Content-Type': 'application/json'},
        )

        # Change port mtu
        port.update(
            nodes={'sp-0': '192.168.1.11/24', 'sp-1': '192.168.1.22/24'}
        )

        # Result: Request with expected parameters was sent to tatlin
        open_url_mock.assert_called_with(**open_url_kwargs)

        # Satisfy Python <= 2.7 & 3.5. It does not have builtin dict order,
        # so resulting json may be in different order than expected
        call_args, call_kwargs = open_url_mock.call_args
        call_data = json.loads(call_kwargs['data'])
        expected_call_data = {
            'params': {
                'nodes': {
                    'sp-0': [{'ipaddress': '192.168.1.11', 'netmask': '24'}],
                    'sp-1': [{'ipaddress': '192.168.1.22', 'netmask': '24'}],
                },
                'failover': get_addrs_for_request(port.virtual_address),
                'gateway': port.gateway,
                'mtu': port.mtu,
            },
        }
        assert_that(call_data, has_entries(expected_call_data))

    def test_waiting_for_connection(
        self, client, mock_method, mocker, open_url_kwargs, ports_response,
    ):
        new_addresses = [
            '192.168.1.2/24',
            '192.168.1.3/24',
            '192.168.1.4/24',
            '192.168.1.5/24',
            '192.168.1.6/24',
        ]

        # Create port object
        port = Port(client=client, port_data=ports_response[1])

        # Mock sleeping
        mock_method(target=PORT_MODULE + '.time.sleep')

        # Mock open_url without data
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Wait interfaces up
        port._wait_interfaces_up(
            new_virtual_address=new_addresses[0],
            nodes={'sp-0': new_addresses[1:3], 'sp-1': new_addresses[3:5]}
        )

        # Defining expected calls parameters
        calls = []
        for address in new_addresses:
            ip = get_ip(address)
            call_args = open_url_kwargs.copy()
            call_args.update(
                method='GET',
                url='https://{0}/{1}'.format(
                    ip,
                    port._ep_status),
            )
            calls.append(mocker.call(**call_args))

        # Result: Request was sent for each interface
        open_url_mock.assert_has_calls(calls=calls, any_order=True)

    @pytest.mark.parametrize(
        'new_address',
        [{'new_virtual_address': '192.168.1.2/24'},
         {'nodes': {'sp-0': '192.168.1.3/24'}}]
    )
    def test_waiting_for_connection_interface_was_not_up(
        self, client, mock_method, open_url_kwargs, new_address, ports_response
    ):
        # Create port object
        port = Port(client=client, port_data=ports_response[1])

        # Mock sleeping
        mock_method(target=PORT_MODULE + '.time.sleep')

        # Mock open_url with exception
        mock_method(
            target=OPEN_URL_FUNC,
            side_effects=RESTClientConnectionError
        )

        # Result: Expected error was raised
        err_msg = r'Interface \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} was not up'
        with pytest.raises(TatlinClientError, match=err_msg):
            port._wait_interfaces_up(**new_address)

    def test_getting_ip_for_reconnect_virt_ip(
        self, client, mock_method, ports_response
    ):
        # Create port object
        port = Port(client=client, port_data=ports_response[1])

        # Set client's host equal to port's virtual address
        virtual_ip = port.virtual_address.ip
        client.set_host(virtual_ip)

        # Get ip for reconnect
        reconnect_ip = port._get_ip_for_reconnect(
            new_virtual_address='192.168.11.1/24',
            nodes={'sp-0': '192.168.2.22/24',
                   'sp-1': '192.168.3.33/24'}
        )

        # Result: IP for reconnect equals to new virtual address
        assert reconnect_ip == '192.168.11.1'

    def test_getting_ip_for_reconnect_sp(
        self, client, mock_method, ports_response,
    ):
        # Create port object
        port = Port(client=client, port_data=ports_response[1])

        # Set client's host equal to port's virtual address
        sp0_ip = port.nodes['sp-0'].addresses[0].ip
        client.set_host(sp0_ip)

        # Get ip for reconnect
        reconnect_ip = port._get_ip_for_reconnect(
            new_virtual_address='192.168.11.1/24',
            nodes={'sp-0': '192.168.2.22/24',
                   'sp-1': '192.168.3.33/24'}
        )

        # Result: IP for reconnect equals to new virtual address
        assert reconnect_ip == '192.168.2.22'

    def test_getting_none_as_ip_for_reconnect(
        self, client, mock_method, ports_response,
    ):
        # Create port object
        port = Port(client=client, port_data=ports_response[1])

        # Get ip for reconnect
        reconnect_ip = port._get_ip_for_reconnect(
            new_virtual_address='192.168.11.1/24',
            nodes={'sp-0': '192.168.2.22/24',
                   'sp-1': '192.168.3.33/24'}
        )

        # Result: IP for reconnect is None
        assert reconnect_ip is None
