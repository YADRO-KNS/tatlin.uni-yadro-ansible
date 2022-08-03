# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.osmgr.port import Port
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.osmgr.ntp import NtpConfig
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.osmgr.dns import DnsConfig
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import PORTS_STATUS_ENDPOINT

try:
    from typing import List, Dict
except ImportError:
    # Satisfy Python 2 which doesn't have typing.
    List = Dict = None


class OsmgrService:

    def __init__(self, client):
        self._client = client
        self._ep_ports_status = PORTS_STATUS_ENDPOINT

    def get_dns_config(self):
        return DnsConfig(client=self._client)

    def get_ntp_config(self):
        return NtpConfig(client=self._client)

    def get_ports(self):  # type: () -> List[Port]
        rv = []
        ports_data = self._client.get(self._ep_ports_status).json
        for port_data in ports_data:
            port = Port(
                client=self._client,
                port_data=port_data,
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
