# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError

try:
    from typing import List
except ImportError:
    List = None


class SnmpConfig:

    def __init__(self, client):
        self._client = client
        self.community = None
        self.servers = []
        self._endpoint = self._client.network_service.SNMP_ENDPOINT

        self.load()

    def add_server(self, server):  # type: (str) -> None
        """
        Args:
             server (str): server address in format IP:port/FQDN:port
        """

        self.update(servers=self.servers + [server])

    def load(self):  # type: () -> None
        snmp_data = self._client.get(self._endpoint).json
        self.community = snmp_data.get('community', None)
        self.servers = list(snmp_data.get('recipients', {}).keys())

    def remove_server(self, server):  # type: (str) -> None
        """
        Args:
             server (str): server address in format IP:port/FQDN:port
               or IP/FQDN

        Note:
            If server is passed without port and tatlin has multiple addresses with same IP,
            but different ports, all addresses with this IP will be removed
        """

        keeping_servers = []
        for old_server in self.servers:
            old_address, old_port = old_server.split(':')
            removing_address, removing_port = server.partition(':')[::2]

            if old_address != removing_address:
                keeping_servers.append(old_server)
            elif removing_port and old_port != removing_port:
                keeping_servers.append(old_server)

        self.update(servers=keeping_servers)

    def reset(self):  # type: () -> None
        self._client.put(
            self._endpoint,
            body=None,
        )

        self.load()

    def update(self, servers=None, community=None):
        # type: (List[str], str) -> None

        if not community and not self.community and servers:
            raise TatlinClientError(
                "Can't update servers if community is None"
            )

        if servers is not None:
            for server in servers:
                if len(server.split(':')) != 2:
                    raise TatlinClientError(
                        'Wrong server address format. '
                        'Must be IP:port or FQDN:port'
                    )

        req_servers = servers if servers is not None else self.servers

        self._client.put(
            self._endpoint,
            body={
                'community': community or self.community,
                'recipients': dict((server, {}) for server in req_servers)
            }
        )

        self.load()
