# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import DNS_CONFIG_ENDPOINT

try:
    from typing import Union, List
except ImportError:
    Union = List = None


class DnsConfig:

    def __init__(self, client):
        self._client = client
        self.servers = []
        self.search_list = []
        self._endpoint = DNS_CONFIG_ENDPOINT

        self.load()

    def add_server(self, server):  # type: (str) -> None
        self.update(servers=self.servers + [server])

    def add_suffix(self, suffix):  # type: (str) -> None
        """Adds DNS suffix to the search list"""
        self.update(search_list=self.search_list + [suffix])

    def load(self):  # type: () -> None
        dns_data = self._client.get(self._endpoint).json

        self.servers = dns_data['dns_static_servers']
        self.search_list = dns_data['dns_static_search_list']

    def remove_server(self, server):  # type: (str) -> None
        self.update(servers=[s for s in self.servers if s != server])

    def remove_suffix(self, suffix):  # type: (str) -> None
        """Removes suffix from the search list"""
        self.update(search_list=[s for s in self.search_list if s != suffix])

    def reset(self):  # type: () -> None
        self.update(servers=[], search_list=[])

    def update(self, servers=None, search_list=None):
        # type: (Union[str, List[str]], Union[str, List[str]]) -> None

        body_servers = servers \
            if servers is not None else self.servers
        body_search_list = search_list \
            if search_list is not None else self.search_list

        body_servers = [body_servers] \
            if isinstance(body_servers, str) else body_servers
        body_search_list = [body_search_list] \
            if isinstance(body_search_list, str) else body_search_list

        self._client.put(
            path=self._endpoint,
            body={
                'dns_static_servers': body_servers,
                'dns_static_search_list': body_search_list,
            }
        )

        self.load()
