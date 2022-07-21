# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    from typing import Union, List, Dict, Tuple, Optional
except ImportError:
    Union = List = Dict = Tuple = Optional = None

import sys
import time
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import (
    TatlinClientError,
    RESTClientConnectionError,
    RESTClientUnauthorized,
)

if sys.version_info[0] >= 3:
    unicode = str


def get_ip_and_mask(address):  # type: (str) -> Tuple[str, str]
    try:
        ip, mask = address.split('/')
    except ValueError:
        raise TatlinClientError(
            'Wrong format of ip address. It should be in '
            '"x.x.x.x/x" format, but was {0}'.format(address)
        )
    return ip, mask


def get_ip_only(addresses):
    # type: (Union[str, List[str]]) -> Union[List[str], str]
    """
    Extracts ip from ip and mask str in 'x.x.x.x/24' format.
    If only one address was passed as string, returns string object.
    If list of addresses was passed, even with single item,
    list object returns
    """

    if isinstance(addresses, list):
        return [get_ip_and_mask(addr)[0] for addr in addresses]
    elif isinstance(addresses, (str, unicode)):
        return get_ip_and_mask(addresses)[0]
    else:
        raise TatlinClientError(
            'Unknown type of addresses was passed: {0}'.format(type(addresses))
        )


class Port:

    def __init__(
        self,
        client,
        name,  # type: str
        port_type,  # type: str
    ):
        self._client = client
        self.name = name
        self.type = port_type
        self.gateway = None
        self.mtu = None
        self.nodes = {}
        self.virtual_address = None
        self._changed_host = ChangedHost(self._client)

        self.load()

    def is_mgmt(self):  # type: () -> bool
        return self.name == 'mgmt'

    def load(self):  # type: () -> None
        all_ports_data = self._client.get(
            self._client.network_service.PORTS_ENDPOINT
        ).json

        port_data = next(
            item for item in all_ports_data if item['id'] == self.name
        )

        failover_data = port_data['params']['failover']
        ip = failover_data[0]['ipaddress'] if failover_data else None
        mask = failover_data[0]['netmask'] if failover_data else None
        self.virtual_address = '/'.join((ip, mask)) \
            if None not in (ip, mask) else ''

        self.gateway = port_data['params']['gateway']
        self.mtu = port_data['params']['mtu']
        self.nodes = self._init_nodes(port_data['params']['nodes'])

    def update(self, virtual_address=None, gateway=None, mtu=None, nodes=None):
        # type: (str, str, int, Dict[str, Union[str, List[str]]]) -> None
        """
        Args:
            virtual_address (str): Ip address with mask in format 'x.x.x.x/x'
            gateway (str): Ip address in format 'x.x.x.x'
            mtu (int): Maximum transmission unit
            nodes (dict): Storage processors' ip addresses with mask in format
                {'sp-0': [x.x.x.x/x], ...}

        Note:
            Values in 'nodes' will rewrite current values. For example,
            if there are addresses 192.168.0.10 and 192.168.0.11 at mgmt port
            for sp-0 and only one address 192.168.0.20 was passed, result
            addresses list will contain single 192.168.0.20
        """

        updating_nodes = nodes.copy() if nodes else {}

        virtual_ip = virtual_mask = None
        if virtual_address or self.virtual_address:
            virtual_ip, virtual_mask = get_ip_and_mask(
                virtual_address or self.virtual_address)

        body_nodes = {}
        for node in self.nodes.values():
            # replace nodes addresses by new addresses if they were passed
            addresses = updating_nodes.pop(node.name) \
                if node.name in updating_nodes else node.addresses

            addresses = [addresses] \
                if isinstance(addresses, str) else addresses

            body_nodes[node.name] = []
            for addr in addresses:
                ip, mask = get_ip_and_mask(addr)
                body_nodes[node.name].append(
                    {'ipaddress': ip, 'netmask': mask}
                )

        if len(updating_nodes) > 0:
            is_plural = len(updating_nodes) > 1
            raise TatlinClientError(
                'There is no {0} {1} on port {2}'.format(
                    'nodes' if is_plural else 'node',
                    ', '.join(updating_nodes.keys()),
                    self.name)
            )

        self._client.post(
            path='{ports_endpoint}/{port_type}/{port_name}'.format(
                ports_endpoint=self._client.network_service.PORTS_ENDPOINT,
                port_type=self.type,
                port_name=self.name,
            ),
            body={
                'params': {
                    'nodes': body_nodes,
                    'failover': [{
                        'ipaddress': virtual_ip,
                        'netmask': virtual_mask,
                    }],
                    'gateway': gateway or self.gateway,
                    'mtu': mtu or self.mtu,
                }
            }
        )

        if self.is_mgmt():
            self._wait_interfaces_up(
                new_virtual_address=virtual_address,
                nodes=nodes,
            )

            ip_for_reconnect = self._get_ip_for_reconnect(
                new_virtual_address=virtual_address,
                nodes=nodes,
            )

            if ip_for_reconnect is not None:
                # Reconnecting to new ip address if it was changed
                self._client.reconnect(host=ip_for_reconnect)

        self.load()

    def _get_ip_for_reconnect(self, new_virtual_address=None, nodes=None):
        # type: (str, Dict[str, Union[str, List[str]]]) -> Optional[str]

        host = self._client.get_host()
        if host is None:
            return

        if new_virtual_address is not None:
            old_virtual_ip = get_ip_only(self.virtual_address)
            new_virtual_ip = get_ip_only(new_virtual_address)

            if host == old_virtual_ip and new_virtual_ip != old_virtual_ip:
                return new_virtual_ip

        if nodes is not None:
            for node_name, new_addresses in nodes.items():
                old_addresses = self.nodes[node_name].addresses
                new_addresses = new_addresses if \
                    isinstance(new_addresses, list) else [new_addresses]

                old_ips = get_ip_only(old_addresses)
                new_ips = get_ip_only(new_addresses)

                if host in old_ips and host not in new_ips:
                    return new_ips[0]

    def _init_nodes(self, nodes_data):
        # type: (Dict) -> Dict[str, Node]
        rv = {}

        for node_name, addresses_data in nodes_data.items():
            addresses = []
            for addr in addresses_data:
                ip, mask = addr.get('ipaddress'), addr.get('netmask')
                addresses.append(
                    '/'.join((ip, mask)) if None not in (ip, mask) else '',
                )

            if node_name in self.nodes:
                rv[node_name] = self.nodes[node_name]
                rv[node_name].addresses = addresses
            else:
                rv[node_name] = Node(
                    client=self._client,
                    port=self,
                    name=node_name,
                    addresses=addresses
                )

        return rv

    def _wait_interfaces_up(self, new_virtual_address=None, nodes=None):
        # type: (str, Dict[str, Union[str, List]]) -> None
        new_ips = []

        if nodes is not None:
            for addresses in nodes.values():
                if isinstance(addresses, str):
                    addresses = [addresses]
                new_ips.extend(get_ip_only(addresses))

        if new_virtual_address is not None:
            new_ips.append(get_ip_only(new_virtual_address))

        if len(new_ips) == 0:
            return

        # Tatlin can reconfigure interfaces with undefined delay after
        # changing ips, and when this happens, it can reset current
        # connection. Because of requests are sent thick and fast, one
        # of them can be sent at the reconfiguration moment and will fail.
        # Sleeping for 5 seconds behaves well at testing, in spite of it's
        # a kind of crutch. If you find better solution, you're welcome to
        # suggest it.
        # Problem was detected with connection to virtual ip and changing it,
        # but it doesn't mean that it can't happen with other addresses
        time.sleep(5)

        attempts = 3
        for ip in new_ips:
            is_up = False
            with self._changed_host(ip):
                for attempt in range(attempts):
                    try:
                        self._client.get(
                            self._client.network_service.PORTS_ENDPOINT)
                        is_up = True
                    except RESTClientUnauthorized:
                        is_up = True
                    except RESTClientConnectionError:
                        time.sleep(0.1)

                    if is_up:
                        break

            if not is_up:
                raise TatlinClientError(
                    'Interface {0} was not up'.format(ip)
                )

    def __repr__(self):
        return 'Port ' + self.name

    def __eq__(self, other):
        return self.name == other.name


class Node:

    def __init__(
        self,
        client,
        port,  # type: Port
        name,  # type: str
        addresses,  # type: List[str]
    ):
        self._client = client
        self.port = port
        self.name = name
        self.addresses = addresses  # TODO: make address an str object with ip and mask attrs

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.name == other.name and self.port == other.port

    def __repr__(self):
        return 'Node {0} on Port {1}'.format(self.name, self.port.name)


class ChangedHost:
    """Temporarily changes host attribute for RestClient"""

    def __init__(self, client):
        self.client = client
        self.init_host = None
        self.new_host = None

    def __call__(self, host):
        self.new_host = host
        return self

    def __enter__(self):
        if self.new_host is None:
            raise TatlinClientError(
                'No host was passed for changed host context manager'
            )

        self.init_host = self.client.get_host()
        self.client.set_host(self.new_host)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.init_host is None:
            raise TatlinClientError(
                'Initial host was not saved for changed host context manager'
            )

        self.client.set_host(self.init_host)
        self.init_host = self.new_host = None
