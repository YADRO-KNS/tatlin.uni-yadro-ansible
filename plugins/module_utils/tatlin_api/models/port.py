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

from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import (
    build_url, PORTS_ENDPOINT)
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import (
    TatlinClientError, RESTClientConnectionError, RESTClientUnauthorized,
)

if sys.version_info[0] >= 3:
    unicode = str


def get_ip_and_mask(address):  # type: (str) -> Tuple[str, str]
    try:
        ip, mask = address.split('/')
    except ValueError:
        raise TatlinClientError(
            'Wrong format of ip address. It should be in '
            '"x.x.x.x/x" format, but was "{0}"'.format(address)
        )
    return ip, mask


def get_ip(addresses):
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

    def __init__(self, client, port_data):
        self._client = client
        self.name = port_data['id']
        self.type = port_data['meta']['type']
        self.gateway = port_data['params']['gateway']
        self.mtu = port_data['params']['mtu']
        self.mac = port_data['params'].get('mac')
        self.wwpn = port_data['params'].get('wwpn')
        self.virtual_address = self._retrieve_virtual_address(
            port_data['params']['failover']
        )

        self.nodes = {}
        self._init_nodes(
            nodes_data=port_data['params']['nodes']
        )

        self._data_role = port_data['meta'].get('data_role', False)
        self._replication_role = port_data['meta'].get(
            'replication_role', False)

        self._changed_host = ChangedHost(self._client)
        self._ep = build_url(PORTS_ENDPOINT, self.type, self.name)
        self._ep_status = build_url(
            PORTS_ENDPOINT, self.type, self.name, 'status',
        )

    def is_mgmt(self):  # type: () -> bool
        return self.name == 'mgmt'

    def load(self):  # type: () -> None
        port_data = self._client.get(self._ep_status).json

        self.gateway = port_data['params']['gateway']
        self.mtu = port_data['params']['mtu']
        self.virtual_address = self._retrieve_virtual_address(
            port_data['params']['failover']
        )
        self._init_nodes(port_data['params']['nodes'])

        self._data_role = port_data['meta'].get('data_role', False)
        self._replication_role = port_data['meta'].get(
            'replication_role', False)

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

        processing_nodes = nodes.copy() if nodes else {}

        virtual_ip = virtual_mask = None
        if virtual_address or self.virtual_address:
            virtual_ip, virtual_mask = get_ip_and_mask(
                virtual_address or str(self.virtual_address)
            )

        nodes_to_send = {}
        for node in self.nodes.values():
            # replace nodes addresses by new addresses if they were passed
            addresses = processing_nodes.pop(node.name, node.addresses_str)
            addresses = [addresses] \
                if isinstance(addresses, str) else addresses

            nodes_to_send[node.name] = []
            for addr in addresses:
                ip, mask = get_ip_and_mask(addr)
                nodes_to_send[node.name].append(
                    {'ipaddress': ip, 'netmask': mask}
                )

        if len(processing_nodes) > 0:
            is_plural = len(processing_nodes) > 1
            raise TatlinClientError(
                'There is no {0} {1} on port {2}'.format(
                    'nodes' if is_plural else 'node',
                    ', '.join(processing_nodes.keys()),
                    self.name)
            )

        self._client.post(
            path=self._ep,
            body={
                'meta': {
                    'data_role': self._data_role,
                    'replication_role': self._replication_role,
                },
                'params': {
                    'nodes': nodes_to_send,
                    'failover': [{
                        'ipaddress': virtual_ip,
                        'netmask': virtual_mask,
                    }],
                    'gateway': gateway if gateway is not None else self.gateway,
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
            old_virtual_ip = getattr(self.virtual_address, 'ip', None)
            new_virtual_ip = get_ip(new_virtual_address)

            if host == old_virtual_ip and new_virtual_ip != old_virtual_ip:
                return new_virtual_ip

        if nodes is not None:
            for node_name, new_addresses in nodes.items():
                old_addresses = self.nodes[node_name].addresses
                new_addresses = new_addresses if \
                    isinstance(new_addresses, list) else [new_addresses]

                old_ips = [addr.ip for addr in old_addresses]
                new_ips = [get_ip(addr) for addr in new_addresses]

                if host in old_ips and host not in new_ips:
                    return new_ips[0]

    def _init_nodes(self, nodes_data):
        # type: (Dict) -> None
        new_nodes = {}

        for node_name, addresses_data in nodes_data.items():
            addresses = []
            for addr in addresses_data:
                ip, mask = addr.get('ipaddress'), addr.get('netmask')

                valid_address = ip and mask
                # Error if only one parameter is filled
                non_valid_address = not valid_address and (ip or mask)

                if valid_address:
                    addresses.append(NodeAddress(
                        ip=ip,
                        mask=mask,
                        address_id=addr.get('ipaddressid'),
                        status=addr.get('status'),
                    ))
                elif non_valid_address:
                    msg = 'empty ipaddress' if not ip else 'empty netmask'
                    raise TatlinClientError(
                        'Failed parse ip address on node {node} '
                        'on port {port}. Wrong format: {msg} '.format(
                            node=node_name,
                            port=self.name,
                            msg=msg,
                        )
                    )

            if node_name in self.nodes:
                new_nodes[node_name] = self.nodes[node_name]
                new_nodes[node_name].addresses = addresses
            else:
                new_nodes[node_name] = Node(
                    client=self._client,
                    port=self,
                    name=node_name,
                    addresses=addresses
                )

        self.nodes = new_nodes

    def _retrieve_virtual_address(self, failover_data):
        # type: (List[Dict]) -> Optional[VirtualAddress]
        ip = failover_data[0]['ipaddress'] if failover_data else None
        mask = failover_data[0]['netmask'] if failover_data else None

        valid_address = ip and mask
        # Error if only one parameter is filled
        non_valid_address = not valid_address and (ip or mask)

        if valid_address:
            return VirtualAddress(ip, mask)
        elif non_valid_address:
            msg = 'empty ipaddress' if not ip else 'empty netmask'
            raise TatlinClientError(
                'Failed parse virtual address on port {port}. '
                'Wrong format: {msg} '.format(
                    port=self.name,
                    msg=msg,
                )
            )

    def _wait_interfaces_up(self, new_virtual_address=None, nodes=None):
        # type: (str, Dict[str, Union[str, List]]) -> None
        new_ips = []

        if nodes is not None:
            for addresses in nodes.values():
                if isinstance(addresses, str):
                    addresses = [addresses]
                new_ips.extend(get_ip(addresses))

        if new_virtual_address is not None:
            new_ips.append(get_ip(new_virtual_address))

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
                        self._client.get(self._ep_status)
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
        if isinstance(other, Port):
            return self.name == other.name
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class Node:

    def __init__(self, client, port, name, addresses):
        # type: ('TatlinClient', Port, str, List[NodeAddress]) -> None
        self._client = client
        self.port = port
        self.name = name
        self.addresses = addresses or []

    @property
    def addresses_str(self):  # type: () -> List[str]
        return [str(addr) for addr in self.addresses]

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.name == other.name and self.port == other.port
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'Node {0} on Port {1}'.format(self.name, self.port.name)


class BaseAddress:
    def __init__(self, ip, mask):  # type: (str, str) -> None
        self.ip = ip
        self.mask = mask

    def __str__(self):
        return '/'.join((self.ip, self.mask))


class NodeAddress(BaseAddress):

    def __init__(self, ip, mask, address_id, status):
        # type: (str, str, str, str) -> None
        super(NodeAddress, self).__init__(ip, mask)
        self.address_id = address_id
        self.status = status

    def __eq__(self, other):
        if isinstance(other, NodeAddress):
            return self.address_id == other.address_id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class VirtualAddress(BaseAddress):

    def __eq__(self, other):
        if isinstance(other, VirtualAddress):
            return self.ip == other.ip and self.mask == other.mask
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


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
