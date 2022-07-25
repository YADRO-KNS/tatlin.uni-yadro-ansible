# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.network.port import Port
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.network.ntp import NtpConfig
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.network.snmp import SnmpConfig
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError

try:
    from typing import List, Dict
except ImportError:
    # Satisfy Python 2 which doesn't have typing.
    List = Dict = None


class NetworkService:
    """
    Note:
        Tatlin doesn't have such service. It's
        just current object model abstraction
    """

    OSMGR_ENDPOINT = 'osmgr'
    NOTIFICATION_ENDPOINT = 'notification'
    VERSION1 = 'v1'
    VERSION2 = 'v2'
    PORTS_ENDPOINT = '/'.join([OSMGR_ENDPOINT, VERSION2, 'ports'])
    NTP_SERVERS_ENDPOINT = '/'.join(
        [OSMGR_ENDPOINT, VERSION1, 'netconfig', 'ntp', 'servers']
    )
    SNMP_ENDPOINT = '/'.join([NOTIFICATION_ENDPOINT, VERSION1, 'handlers', 'snmp'])

    def __init__(self, client):
        self._client = client

    def get_ntp_config(self):
        return NtpConfig(client=self._client)

    def get_ports(self):  # type: () -> List[Port]
        rv = []
        ports_data = self._client.get(self.PORTS_ENDPOINT).json
        for item in ports_data:
            port = Port(
                client=self._client,
                name=item['id'],
                port_type=item['meta']['type'],
            )
            rv.append(port)

        return rv

    def get_port(self, name):  # type: (str) -> Port
        ports = self.get_ports()
        port = next((port for port in ports if port.name == name), None)

        if port is None:
            raise TatlinClientError(
                'Not found port with name {0}'.format(name),
            )

        return port

    def get_snmp_config(self):
        return SnmpConfig(client=self._client)
