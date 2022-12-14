# -*- coding: utf-8 -*-

# YADRO Tatlin Unified Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.endpoints import NTP_SERVERS_ENDPOINT

try:
    from typing import List
except ImportError:
    # Satisfy Python 2 which doesn't have typing.
    List = None


class NtpConfig:

    def __init__(self, client):
        self._client = client
        self.servers = []
        self._servers_endpoint = NTP_SERVERS_ENDPOINT

        self.load()

    def add_server(self, server):  # type: (str) -> None
        self.set_servers(self.servers + [server])

    def load(self):  # type: () -> None
        data = self._client.get(self._servers_endpoint).json
        self.servers = data['ntp_server_list']

    def remove_server(self, server):  # type: (str) -> None
        self.set_servers([s for s in self.servers if s != server])

    def reset_servers(self):
        self.set_servers([])

    def set_servers(self, servers):  # type: (List) -> None
        self._client.put(
            self._servers_endpoint,
            body={'ntp_server_list': servers},
        )
        self.load()
