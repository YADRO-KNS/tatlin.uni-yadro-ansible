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
module: tatlin_sp_port
short_description: Configure data port
version_added: "1.0.0"
description:
  - This module is intended to configure specified data port
  - Supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin.connection_options
options:
  name:
    required: True
    type: str
    description: Name of the port
  gateway:
    required: False
    type: str
    description: Ip address of default gateway
  nodes:
    required: False
    type: list
    elements: dict
    description:
      - List of storage processors with corresponding ip addresses
    suboptions:
      name:
        required: True
        type: str
        description: Name of the Storage Processor
      address:
        required: True
        type: dict
        description: Ip address of the SP with mask
        suboptions:
          ip:
            required: True
            type: str
            description: Ip address of the SP
          mask:
            required: True
            type: str
            description: Mask of the ip address
  state:
    type: str
    choices: [present, absent]
    default: present
    description:
      - C(present) configures port's corresponding parameters
      - C(absent) resets port's configuration
notes:
  - For configuring mgmt port it is recommended
    to use M(yadro.tatlin.tatlin_sp_mgmt_port)
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
- name: Configure p00
  yadro.tatlin.tatlin_sp_port:
    connection: "{{ connection }}"
    name: p00
    gateway: 192.168.1.1
    nodes:
      - name: sp-0
        address:
          ip: 192.168.1.2
          mask: 24
      - name: sp-1
        address:
          ip: 192.168.1.3
          mask: 24

- name: Test port change | Reset p00
  yadro.tatlin.tatlin_sp_port:
    connection: "{{ connection }}"
    name: p00
    state: absent
"""


from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_module import TatlinModule


class TatlinPortModule(TatlinModule):

    def __init__(self):
        argument_spec = {
            'name': {'type': 'str', 'required': True},
            'gateway': {'type': 'str', 'required': False},
            'nodes': {
                'type': 'list',
                'elements': 'dict',
                'required': False,
                'options': {
                    'name': {'type': 'str', 'required': True},
                    'address': {
                        'type': 'dict',
                        'required': True,
                        'options': {
                            'ip': {'type': 'str', 'required': True},
                            'mask': {'type': 'str', 'required': True},
                        },
                    },
                },
            },
            'state': {
                'type': 'str',
                'required': False,
                'default': 'present',
                'choices': ['present', 'absent'],
            },
        }

        super(TatlinPortModule, self).__init__(
            argument_spec=argument_spec,
            supports_check_mode=True,
        )

    def run(self):
        port = self.tatlin.get_port(self.params['name'])
        port_changes = self.get_port_changes(port)

        if len(port_changes) > 0:
            if not self.check_mode:
                port.update(**port_changes)

            self.exit_json(msg='Operation successful', changed=True)
        else:
            self.exit_json(msg='No changes required', changed=False)

    def get_port_changes(self, port):
        rv = {}

        if self.params['state'] == 'present':
            old_gateway = port.gateway
            new_gateway = self.params['gateway']
            if new_gateway is not None and new_gateway != old_gateway:
                rv['gateway'] = self.params['gateway']

            if self.params['nodes'] is not None:
                nodes_changes = {}
                for node in self.params['nodes']:
                    self.check_node_exists(port, node['name'])

                    old_address = \
                        (port.nodes[node['name']].addresses_str or [None])[0]

                    new_address = '{0}/{1}'.format(
                        node['address']['ip'], node['address']['mask'])

                    if old_address != new_address:
                        nodes_changes[node['name']] = new_address

                if len(nodes_changes) > 0:
                    rv['nodes'] = nodes_changes

        else:  # state absent
            if port.gateway != '':
                rv['gateway'] = ''

            need_reset_nodes = any(
                len(node.addresses) > 0 for node in port.nodes.values()
            )

            if need_reset_nodes:
                rv['nodes'] = {}
                for node in port.nodes.keys():
                    rv['nodes'][node] = []

        return rv

    def check_node_exists(self, port, node_name):
        if node_name not in port.nodes:
            self.fail_json(
                msg='There is no node {node} on port {port}'.format(
                    node=node_name, port=port.name),
                error="Node doesn't exist",
                changed=False,
            )


def main():
    TatlinPortModule()


if __name__ == "__main__":
    main()
