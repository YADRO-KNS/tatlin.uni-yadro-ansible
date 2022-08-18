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
module: tatlin_sp_snmp
short_description: Configure SP SNMP settings
version_added: "1.0.0"
description:
  - This module is intended to configure SNMP servers` URIs (IP address or
    domain name & port) list and community name
  - This module supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin.connection_options
options:
  community:
    type: str
    required: False
    description: SNMP community name
  servers:
    type: list
    elements: dict
    required: False
    description: SNMP servers` addresses
    suboptions:
      ip:
        type: str
        required: True
        description: ip address of trap receiver
      port:
        type: str
        required: True
        description: port of trap recevier
  state:
    type: str
    choices: [present, absent]
    default: present
    description:
      - C(present) sets listed SNMP servers and community name
      - C(absent) deletes listed SNMP servers
      - If no servers listed with C(absent) all servers addresses
        and community name will be removed
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
- name: Set SNMP config
  yadro.tatlin.tatlin_sp_snmp:
    connection: "{{ connection }}"
    community: tatlin
    servers:
      - ip: 127.0.1.2
        port: 162
      - ip: example.com
        port: 162
    state: present

- name: Remove SNMP server
  yadro.tatlin.tatlin_sp_snmp:
    connection: "{{ connection }}"
    servers:
      - ip: example.com
        port: 162
    state: absent

- name: Reset config
  yadro.tatlin.tatlin_sp_snmp:
    connection: "{{ connection }}"
    state: absent
"""


from functools import partial
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_module import TatlinModule


class TatlinSnmpModule(TatlinModule):

    def __init__(self):
        argument_spec = {
            'community': {'type': 'str', 'required': False},
            'servers': {
                'type': 'list',
                'elements': 'dict',
                'required': False,
                'options': {
                    'ip': {'type': 'str', 'required': True},
                    'port': {'type': 'str', 'required': True},
                },
            },
            'state': {
                'type': 'str',
                'required': False,
                'default': 'present',
                'choices': ['present', 'absent'],
            },
        }

        super(TatlinSnmpModule, self).__init__(
            argument_spec=argument_spec,
            supports_check_mode=True,
        )

        if self.params['state'] == 'absent' \
                and self.params['community'] is not None:
            self.fail_json(
                changed=False,
                error='Mutually exclusive parameters',
                msg='It is prohibited to define community '
                    'as not None and state as absent',
            )

    def run(self):
        action = None
        snmp_config = self.tatlin.get_snmp_config()

        if self.params['state'] == 'absent' and \
           self.params['servers'] is None and \
           (snmp_config.community is not None or len(snmp_config.servers) > 0):
            action = snmp_config.reset
        else:
            changes = self.get_changes(snmp_config)
            if len(changes) > 0:
                action = partial(
                    snmp_config.update,
                    **changes)

        if not action:
            self.exit_json(msg='No changes required', changed=False)

        if not self.check_mode:
            action()

        self.exit_json(msg='Operation successful', changed=True)

    def get_changes(self, snmp_config):
        rv = {}

        state_present = self.params['state'] == 'present'
        new_community = self.params['community']
        if new_community is not None and state_present \
                and new_community != snmp_config.community:
            rv['community'] = new_community

        if self.params['servers'] is not None:
            input_servers = [
                ':'.join((s['ip'], s['port'])) for s in self.params['servers']
            ]

            if state_present:
                if not same_servers(snmp_config.servers, input_servers):
                    rv['servers'] = input_servers
            else:
                desired_servers = [server for server in snmp_config.servers
                                   if server not in input_servers]

                if not same_servers(snmp_config.servers, desired_servers):
                    rv['servers'] = desired_servers

        return rv


def same_servers(servers1, servers2):
    return sorted(servers1) == sorted(servers2)


def main():
    TatlinSnmpModule()


if __name__ == "__main__":
    main()
