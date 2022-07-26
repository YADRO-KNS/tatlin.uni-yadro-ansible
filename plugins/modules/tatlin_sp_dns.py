#!/usr/bin/python
# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r"""
---
module: tatlin_sp_dns
short_description: Configure SP DNS settings
version_added: "1.0.0"
description:
  - This module is intended to configure DNS servers and DNS search list
  - This module supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin.connection_options
options:
  servers:
    type: list
    elements: str
    required: False
    description: List of DNS servers` addresses in format x.x.x.x
  search_list:
    type: list
    elements: str
    required: False
    description: List of DNS suffixes
  state:
    type: str
    choices: [present, absent]
    default: present
    description:
      - C(present) sets listed DNS servers or DNS search list or both
      - C(absent) deletes listed DNS servers or DNS search list or both
      - If no servers and no DNS suffixes listed with C(absent) all
        servers addresses and DNS search list will be removed
"""

RETURN = r"""
---
msg:
  type: str
  returned: always
  description: Operation status message
error:
  type: str
  returned: on error
  description: Error details if raised
"""

EXAMPLES = r"""
---
- name: Set DNS config
  yadro.tatlin.tatlin_sp_dns:
    connection: "{{ connection }}"
    servers:
      - 127.0.0.1
      - 1.1.1.1
    search_list:
      - example.com
      - test.com

- name: Remove server
  yadro.tatlin.tatlin_sp_dns:
    connection: "{{ connection }}"
    servers:
      - 1.1.1.1
    state: absent

- name: Remove suffix
  yadro.tatlin.tatlin_sp_dns:
    connection: "{{ connection }}"
    search_list:
      - test.com
    state: absent

- name: Clear config
  yadro.tatlin.tatlin_sp_dns:
    connection: "{{ connection }}"
    state: absent
"""


from functools import partial
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_module import TatlinModule


class TatlinDnsModule(TatlinModule):

    def __init__(self):
        argument_spec = {
            'servers': {'type': 'list', 'elements': 'str', 'required': False},
            'search_list': {
                'type': 'list',
                'elements': 'str',
                'required': False,
            },
            'state': {
                'type': 'str',
                'required': False,
                'default': 'present',
                'choices': ['present', 'absent'],
            },
        }

        super(TatlinDnsModule, self).__init__(
            argument_spec=argument_spec,
            supports_check_mode=True,
        )

    def _run(self):
        action = None
        dns_config = self.tatlin_api.osmgr_service.get_dns_config()

        if self.params['state'] == 'absent' and \
           self.params['servers'] is None and \
           self.params['search_list'] is None:

            if len(dns_config.servers) > 0 or len(dns_config.search_list) > 0:
                action = dns_config.reset

        else:
            changes = self.get_changes(dns_config)
            if len(changes) > 0:
                action = partial(dns_config.update, **changes)

        if not action:
            self.exit_json(msg='No changes required', changed=False)

        if not self.check_mode:
            action()

        self.exit_json(msg='Operation successful', changed=True)

    def get_changes(self, dns_config):
        rv = {}

        if self.params['state'] == 'present':
            if not same_lists(
                    self.params['servers'] or [],
                    dns_config.servers
            ):
                rv['servers'] = self.params['servers']

            if not same_lists(
                    self.params['search_list'] or [],
                    dns_config.search_list
            ):
                rv['search_list'] = self.params['search_list']
        else:
            desired_servers = [
                server for server in dns_config.servers
                if server not in (self.params['servers'] or [])
            ]

            if not same_lists(desired_servers, dns_config.servers):
                rv['servers'] = desired_servers

            desired_search_list = [
                item for item in dns_config.search_list
                if item not in (self.params['search_list'] or [])
            ]

            if not same_lists(desired_search_list, dns_config.search_list):
                rv['search_list'] = desired_search_list

        return rv


def same_lists(list1, list2):
    return sorted(list1) == sorted(list2)


def main():
    TatlinDnsModule().run()


if __name__ == "__main__":
    main()
