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
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import check_object
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import (
    OPEN_URL_FUNC,
    PORT_CLASS,
    PORT_MODULE,
)
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.network.port import (
    get_ip_and_mask,
    get_ip_only,
    Port,
    Node,
    ChangedHost,
)
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import (
    RESTClientConnectionError,
    TatlinClientError,
)


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


def get_addrs_for_request(*addresses):
    rv = []

    for addr in addresses:
        ip = mask = None
        if addr:
            ip, mask = get_ip_and_mask(addr)
        rv.append({'ipaddress': ip, 'netmask': mask})

    return rv


class TestPort:

    def test_get_ip_and_mask(self):
        ip, mask = get_ip_and_mask('192.168.0.31/30')
        assert ip == '192.168.0.31'
        assert mask == '30'

    def test_get_ip_only_one_address_str(self):
        ip = get_ip_only('192.168.0.31/30')
        assert type(ip) == str
        assert ip == '192.168.0.31'

    def test_get_ip_only_one_address_list(self):
        ip = get_ip_only(['192.168.0.31/30'])
        assert type(ip) == list
        assert ip == ['192.168.0.31']

    def test_get_ip_only_two_addresses(self):
        ip = get_ip_only(['192.168.0.31/30', '192.168.20.100/30'])
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

    def test_port_is_mgmt_true(self, client, mock_method):
        # Mock method load
        mock_method(target=PORT_CLASS + '.load')

        # Create mgmt port
        port = Port(client=client, name='mgmt', port_type='ip')

        # Get port mgmt status
        is_mgmt = port.is_mgmt()

        # Result: port is mgmt
        assert is_mgmt is True

    def test_port_is_mgmt_false(self, client, mock_method):
        # Mock method load
        mock_method(target=PORT_CLASS + '.load')

        # Create data port
        port = Port(client=client, name='p01', port_type='ip')

        # Get port mgmt status
        is_mgmt = port.is_mgmt()

        # Result: port is not mgmt
        assert is_mgmt is False

    def test_port_load_with_addresses(self, client, mock_method):
        # Save load method for future use
        init_load = Port.load

        # Mock method load without data
        mock_method(target=PORT_CLASS + '.load')

        # Create port
        port = Port(client=client, name='mgmt', port_type='ip')

        # Ensure that port has empty attributes
        check_object(
            port,
            dict(gateway=None, mtu=None, nodes={}, virtual_address=None),
        )

        # Restore load method
        Port.load = init_load

        # Mock open_url with data
        mock_method(OPEN_URL_FUNC, *get_ports_response())

        # Load port
        port.load()

        # Define expected port
        expected_port = {
            'name': 'mgmt',
            'type': 'ip',
            'gateway': '***REMOVED***',
            'mtu': 1500,
            'nodes': {
                "sp-0": Node(client, port, 'sp-0', ['***REMOVED***/24']),
                "sp-1": Node(client, port, 'sp-1', ['***REMOVED***/24'])},
            'virtual_address': '***REMOVED***/24',
        }

        # Result: Port has expected attributes
        check_object(port, expected_port)

        # Additional check, because addresses actually don't
        # checked at the above checking
        # Result: Nodes with expected params was returned
        check_object(
            port.nodes['sp-0'],
            dict(name='sp-0', addresses=['***REMOVED***/24']),
        )
        check_object(
            port.nodes['sp-1'],
            dict(name='sp-1', addresses=['***REMOVED***/24']),
        )

    def test_port_load_wo_addresses(self, client, mock_method):
        # Save load method for future use
        init_load = Port.load

        # Mock method load without data
        mock_method(target=PORT_CLASS + '.load')

        # Create port
        port = Port(client=client, name='p01', port_type='ip')

        # Ensure that port has empty attributes
        check_object(
            port,
            dict(gateway=None, mtu=None, nodes={}, virtual_address=None),
        )

        # Restore load method
        Port.load = init_load

        # Mock open_url with data
        mock_method(OPEN_URL_FUNC, *get_ports_response())

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
            'virtual_address': ''
        }

        # Result: Port has expected attributes
        check_object(port, expected_port)

        # Additional check, because addresses actually don't
        # checked at the above checking
        # Result: Nodes with expected params was returned
        check_object(
            port.nodes['sp-0'],
            dict(name='sp-0', addresses=[]),
        )
        check_object(
            port.nodes['sp-1'],
            dict(name='sp-1', addresses=[]),
        )

    @pytest.mark.parametrize('port_name', ['mgmt', 'p01'])
    def test_update_mtu(
        self, client, mock_method, open_url_kwargs, port_name, mocker,
    ):
        # Mock open_url with data
        mock_method(OPEN_URL_FUNC, *get_ports_response())

        # Create port object
        port = Port(client=client, name=port_name, port_type='ip')

        # Mock load method without data
        mock_method(PORT_CLASS + '.load')

        # Mock open_url method
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Defining expected call parameters
        open_url_kwargs.update(
            method='POST',
            url='https://localhost/{0}/{1}/{2}'.format(
                client.network_service.PORTS_ENDPOINT,
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
        self, client, mock_method, open_url_kwargs, port_name, mocker,
    ):
        # Mock open_url with data
        mock_method(OPEN_URL_FUNC, *get_ports_response())

        # Create port object
        port = Port(client=client, name=port_name, port_type='ip')

        # Mock load method without data
        mock_method(PORT_CLASS + '.load')

        # Mock open_url method
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Defining expected call parameters
        open_url_kwargs.update(
            method='POST',
            url='https://localhost/{0}/{1}/{2}'.format(
                client.network_service.PORTS_ENDPOINT,
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
        self, client, mock_method, open_url_kwargs, port_name, mocker,
    ):
        # Mock open_url with data
        mock_method(OPEN_URL_FUNC, *get_ports_response())

        # Create port object
        port = Port(client=client, name=port_name, port_type='ip')

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
                client.network_service.PORTS_ENDPOINT,
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
                'failover': get_addrs_for_request('192.168.1.111/24'),
                'gateway': port.gateway,
                'mtu': port.mtu,
            },
        }
        assert_that(call_data, has_entries(expected_call_data))

    @pytest.mark.parametrize('port_name', ['mgmt', 'p01'])
    def test_update_sp_addresses(
        self, client, mock_method, open_url_kwargs, port_name, mocker
    ):
        # Mock open_url with data
        mock_method(OPEN_URL_FUNC, *get_ports_response())

        # Create port object
        port = Port(client=client, name=port_name, port_type='ip')

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
                client.network_service.PORTS_ENDPOINT,
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
                    'sp-0': get_addrs_for_request('192.168.1.11/24'),
                    'sp-1': get_addrs_for_request('192.168.1.22/24'),
                },
                'failover': get_addrs_for_request(port.virtual_address),
                'gateway': port.gateway,
                'mtu': port.mtu,
            },
        }
        assert_that(call_data, has_entries(expected_call_data))

    def test_waiting_for_connection(
        self, client, mock_method, mocker, open_url_kwargs,
    ):
        new_addresses = [
            '192.168.1.2/24',
            '192.168.1.3/24',
            '192.168.1.4/24',
            '192.168.1.5/24',
            '192.168.1.6/24',
        ]

        # Mock open_url with data
        mock_method(OPEN_URL_FUNC, *get_ports_response())

        # Create port object
        port = Port(client=client, name='mgmt', port_type='ip')

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
            ip = get_ip_only(address)
            call_args = open_url_kwargs.copy()
            call_args.update(
                method='GET',
                url='https://{0}/{1}'.format(
                    ip,
                    client.network_service.PORTS_ENDPOINT),
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
        self, client, mock_method, open_url_kwargs, new_address,
    ):
        # Mock open_url with data
        mock_method(OPEN_URL_FUNC, *get_ports_response())

        # Create port object
        port = Port(client=client, name='mgmt', port_type='ip')

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

    def test_getting_ip_for_reconnect_virt_ip(self, client, mock_method):
        # Mock open_url with data
        mock_method(OPEN_URL_FUNC, *get_ports_response())

        # Create port object
        port = Port(client=client, name='mgmt', port_type='ip')

        # Set client's host equal to port's virtual address
        virtual_ip = get_ip_only(port.virtual_address)
        client.set_host(virtual_ip)

        # Get ip for reconnect
        reconnect_ip = port._get_ip_for_reconnect(
            new_virtual_address='192.168.11.1/24',
            nodes={'sp-0': '192.168.2.22/24',
                   'sp-1': '192.168.3.33/24'}
        )

        # Result: IP for reconnect equals to new virtual address
        assert reconnect_ip == '192.168.11.1'

    def test_getting_ip_for_reconnect_sp(self, client, mock_method):
        # Mock open_url with data
        mock_method(OPEN_URL_FUNC, *get_ports_response())

        # Create port object
        port = Port(client=client, name='mgmt', port_type='ip')

        # Set client's host equal to port's virtual address
        sp0_ip = get_ip_only(port.nodes['sp-0'].addresses[0])
        client.set_host(sp0_ip)

        # Get ip for reconnect
        reconnect_ip = port._get_ip_for_reconnect(
            new_virtual_address='192.168.11.1/24',
            nodes={'sp-0': '192.168.2.22/24',
                   'sp-1': '192.168.3.33/24'}
        )

        # Result: IP for reconnect equals to new virtual address
        assert reconnect_ip == '192.168.2.22'

    def test_getting_none_as_ip_for_reconnect(self, client, mock_method):
        # Mock open_url with data
        mock_method(OPEN_URL_FUNC, *get_ports_response())

        # Create port object
        port = Port(client=client, name='mgmt', port_type='ip')

        # Get ip for reconnect
        reconnect_ip = port._get_ip_for_reconnect(
            new_virtual_address='192.168.11.1/24',
            nodes={'sp-0': '192.168.2.22/24',
                   'sp-1': '192.168.3.33/24'}
        )

        # Result: IP for reconnect is None
        assert reconnect_ip is None
