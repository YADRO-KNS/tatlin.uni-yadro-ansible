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
    OPEN_URL_FUNC, PORT_CLASS, MODELS_PACKAGE,
)
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import PORTS_ENDPOINT
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.models.port import (
    get_ip_and_mask, get_ip, Port, Node, VirtualAddress, ChangedHost)
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import (
    RESTClientConnectionError, TatlinClientError)


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

    def test_changed_host(self, tatlin):
        # Create context manager
        changed_host = ChangedHost(client=tatlin)

        # Ensure that we use specific host
        assert tatlin.get_connection_host() == 'localhost'

        # Change client's host
        with changed_host('new_host'):
            assert tatlin.get_connection_host() == 'new_host'

        # Result: init host is used after context manager
        assert tatlin.get_connection_host() == 'localhost'

    def test_get_ports(
        self, tatlin, make_mock, ports_response, exp_addrs_sp0, exp_addrs_sp1,
    ):
        # Mock open_url response for get_ports
        make_mock(OPEN_URL_FUNC, return_value=ports_response)

        # Call get_ports
        ports = tatlin.get_ports()

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
             'nodes': {"sp-0": Node(tatlin, p01_port, 'sp-0', []),
                       "sp-1": Node(tatlin, p01_port, 'sp-1', [])},
             'virtual_address': None},
            {'name': 'mgmt',
             'type': 'ip',
             'gateway': '***REMOVED***',
             'mtu': 1500,
             'nodes': {
                 "sp-0": Node(tatlin, mgmt_port, 'sp-0', exp_addrs_sp0),
                 "sp-1": Node(tatlin, mgmt_port, 'sp-1', exp_addrs_sp1),
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
        self, tatlin, make_mock, ports_response, exp_addrs_sp0, exp_addrs_sp1,
    ):
        # Mock open_url response for get_ports
        make_mock(OPEN_URL_FUNC, return_value=ports_response)

        # Call get_port
        mgmt_port = tatlin.get_port('mgmt')

        expected_ports = [
            {'name': 'mgmt',
             'type': 'ip',
             'gateway': '***REMOVED***',
             'mtu': 1500,
             'nodes': {
                 "sp-0": Node(tatlin, mgmt_port, 'sp-0', exp_addrs_sp0),
                 "sp-1": Node(tatlin, mgmt_port, 'sp-1', exp_addrs_sp1)},
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

    def test_get_non_existing_port(self, tatlin, make_mock, ports_response):
        # Mock open_url response for get_ports
        make_mock(OPEN_URL_FUNC, return_value=ports_response)

        # Call get_port
        with pytest.raises(TatlinClientError) as exc_info:
            tatlin.get_port('AbsentPort')

        assert str(exc_info.value) == 'Not found port with name AbsentPort'

    def test_port_is_mgmt_true(self, tatlin, make_mock, ports_response):
        # Create mgmt port
        port = Port(client=tatlin, port_data=ports_response[1])

        # Get port mgmt status
        is_mgmt = port.is_mgmt()

        # Result: port is mgmt
        assert is_mgmt is True

    def test_port_is_mgmt_false(self, tatlin, make_mock, ports_response):
        # Create data port
        port = Port(client=tatlin, port_data=ports_response[0])

        # Get port mgmt status
        is_mgmt = port.is_mgmt()

        # Result: port is not mgmt
        assert is_mgmt is False

    def test_port_load_with_addresses(
        self, tatlin, make_mock, ports_response,
        exp_addrs_sp0, exp_addrs_sp1,
    ):
        # Create port with empty data
        port = Port(client=tatlin, port_data={
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
                nodes={'sp-0': Node(tatlin, port, 'sp-0', []),
                       'sp-1': Node(tatlin, port, 'sp-1', [])},
                virtual_address=None
            ),
        )

        # Mock open_url with data
        make_mock(OPEN_URL_FUNC, return_value=ports_response[1])

        # Load port
        port.load()

        # Define expected port
        expected_port = {
            'name': 'mgmt',
            'type': 'ip',
            'gateway': '***REMOVED***',
            'mtu': 1500,
            'nodes': {
                "sp-0": Node(tatlin, port, 'sp-0', exp_addrs_sp0),
                "sp-1": Node(tatlin, port, 'sp-1', exp_addrs_sp1)},
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
        self, tatlin, make_mock, ports_response
    ):
        # Create port with empty data
        port = Port(client=tatlin, port_data={
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
                nodes={'sp-0': Node(tatlin, port, 'sp-0', []),
                       'sp-1': Node(tatlin, port, 'sp-1', [])},
                virtual_address=None
            ),
        )

        # Mock open_url with data
        make_mock(OPEN_URL_FUNC, return_value=ports_response[0])

        # Load port
        port.load()

        # Define expected port
        expected_port = {
            'name': 'p01',
            'type': 'ip',
            'gateway': '',
            'mtu': 1500,
            'nodes': {"sp-0": Node(tatlin, port, 'sp-0', []),
                      "sp-1": Node(tatlin, port, 'sp-1', [])},
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
        self, tatlin, make_mock, open_url_kwargs,
        port_name, mocker, ports_response,
    ):
        # Create port object
        port_data = next(data for data in ports_response
                         if data['id'] == port_name)

        port = Port(client=tatlin, port_data=port_data)

        # Mock load method without data
        make_mock(PORT_CLASS + '.load')

        # Mock open_url method
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

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
        self, tatlin, make_mock, open_url_kwargs,
        port_name, mocker, ports_response,
    ):
        # Create port object
        port_data = next(data for data in ports_response
                         if data['id'] == port_name)

        port = Port(client=tatlin, port_data=port_data)

        # Mock load method without data
        make_mock(PORT_CLASS + '.load')

        # Mock open_url method
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

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
        self, tatlin, make_mock, open_url_kwargs,
        port_name, mocker, ports_response,
    ):
        # Create port object
        port_data = next(data for data in ports_response
                         if data['id'] == port_name)

        port = Port(client=tatlin, port_data=port_data)

        # Mock load method without data
        make_mock(PORT_CLASS + '.load')

        # Mock open_url method
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Mock waiting interfaces method
        make_mock(target=PORT_CLASS + '._wait_interfaces_up')

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
        self, tatlin, make_mock, open_url_kwargs,
        port_name, mocker, ports_response,
    ):
        # Create port object
        port_data = next(data for data in ports_response
                         if data['id'] == port_name)

        port = Port(client=tatlin, port_data=port_data)

        # Mock load method without data
        make_mock(PORT_CLASS + '.load')

        # Mock open_url method
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Mock waiting interfaces method
        make_mock(target=PORT_CLASS + '._wait_interfaces_up')

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
        self, tatlin, make_mock, mocker, open_url_kwargs, ports_response,
    ):
        new_addresses = [
            '192.168.1.2/24',
            '192.168.1.3/24',
            '192.168.1.4/24',
            '192.168.1.5/24',
            '192.168.1.6/24',
        ]

        # Create port object
        port = Port(client=tatlin, port_data=ports_response[1])

        # Mock sleeping
        make_mock(target=MODELS_PACKAGE + '.port.time.sleep')

        # Mock open_url without data
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

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
        self, tatlin, make_mock, open_url_kwargs, new_address, ports_response
    ):
        # Create port object
        port = Port(client=tatlin, port_data=ports_response[1])

        # Mock sleeping
        make_mock(target=MODELS_PACKAGE + '.port.time.sleep')

        # Mock open_url with exception
        make_mock(
            target=OPEN_URL_FUNC,
            side_effect=RESTClientConnectionError
        )

        # Result: Expected error was raised
        err_msg = r'Interface \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} was not up'
        with pytest.raises(TatlinClientError, match=err_msg):
            port._wait_interfaces_up(**new_address)

    def test_getting_ip_for_reconnect_virt_ip(
        self, tatlin, make_mock, ports_response
    ):
        # Create port object
        port = Port(client=tatlin, port_data=ports_response[1])

        # Set client's host equal to port's virtual address
        virtual_ip = port.virtual_address.ip
        tatlin.set_connection_host(virtual_ip)

        # Get ip for reconnect
        reconnect_ip = port._get_ip_for_reconnect(
            new_virtual_address='192.168.11.1/24',
            nodes={'sp-0': '192.168.2.22/24',
                   'sp-1': '192.168.3.33/24'}
        )

        # Result: IP for reconnect equals to new virtual address
        assert reconnect_ip == '192.168.11.1'

    def test_getting_ip_for_reconnect_sp(
        self, tatlin, make_mock, ports_response,
    ):
        # Create port object
        port = Port(client=tatlin, port_data=ports_response[1])

        # Set client's host equal to port's virtual address
        sp0_ip = port.nodes['sp-0'].addresses[0].ip
        tatlin.set_connection_host(sp0_ip)

        # Get ip for reconnect
        reconnect_ip = port._get_ip_for_reconnect(
            new_virtual_address='192.168.11.1/24',
            nodes={'sp-0': '192.168.2.22/24',
                   'sp-1': '192.168.3.33/24'}
        )

        # Result: IP for reconnect equals to new virtual address
        assert reconnect_ip == '192.168.2.22'

    def test_getting_none_as_ip_for_reconnect(
        self, tatlin, make_mock, ports_response,
    ):
        # Create port object
        port = Port(client=tatlin, port_data=ports_response[1])

        # Get ip for reconnect
        reconnect_ip = port._get_ip_for_reconnect(
            new_virtual_address='192.168.11.1/24',
            nodes={'sp-0': '192.168.2.22/24',
                   'sp-1': '192.168.3.33/24'}
        )

        # Result: IP for reconnect is None
        assert reconnect_ip is None
