#!/usr/bin/python
# -*- coding: utf-8 -*-

# YADRO Tatlin Unified Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r"""
---
module: tatlin_sp_mgmt_port
short_description: Configure SP network settings
version_added: "1.0.0"
description:
  - This module is intended to configure management port
  - Supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin_uni.connection_options
options:
  nodes:
    required: False
    type: list
    elements: dict
    description:
      - List of storage processors with corresponding ip addresses
      - Listed addresses will replace all addresses of storage processor.
        For example, if there are addresses 192.168.0.10 and 192.168.0.11
        at sp-0 and only one address 192.168.0.20 was passed,
        result addresses list will contain single 192.168.0.20
    suboptions:
      name:
        required: True
        type: str
        description: Name of Storage Processor
      addresses:
        required: True
        type: list
        elements: dict
        description:
          - List of ip addresses with mask
        suboptions:
          ip:
            required: True
            type: str
            description: Ip address of Storage Processor
          mask:
            required: True
            type: str
            description: Ip address mask
  gateway:
    required: False
    type: str
    description: Ip address of default gateway
  mtu:
    required: False
    type: int
    description: Maximum transmission unit
  virtual_address:
    required: False
    type: dict
    description:
      - Storage Processor's virtual ip with mask
    suboptions:
      ip:
        required: True
        type: str
        description: Virtual ip address of Storage Processor
      mask:
        required: True
        type: str
        description: Virtual ip address mask
notes:
  - If connection address will be changed by this module, connection will be lost.
    If there are further tasks that must be executed setting new connection address
    by set_fact may be used. Also connection address in inventory will no longer be relevant
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
- name: Update mgmt port settings
  yadro.tatlin_uni.tatlin_sp_mgmt_port:
    connection: "{{ connection }}"
    nodes:
      - name: sp-0
        addresses:
          - ip: 192.168.0.2
            mask: 24
          - ip: 192.168.0.3
            mask: 24
      - name: sp-1
        addresses:
          - ip: 192.168.0.4
            mask: 24
          - ip: 192.168.0.5
            mask: 24
    gateway: 192.168.0.1
    mtu: 1500
    virtual_address:
      ip: 192.168.0.6
      mask: 24
"""


from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_module import TatlinModule


class TatlinMgmtPortModule(TatlinModule):

    def __init__(self):
        argument_spec = {
            'nodes': {
                'type': 'list',
                'elements': 'dict',
                'required': False,
                'options': {
                    'name': {'type': 'str', 'required': True},
                    'addresses': {
                        'type': 'list',
                        'elements': 'dict',
                        'required': True,
                        'options': {
                            'ip': {'type': 'str', 'required': True},
                            'mask': {'type': 'str', 'required': True},
                        }
                    }
                },
            },
            'gateway': {'type': 'str', 'required': False},
            'mtu': {'type': 'int', 'required': False},
            'virtual_address': {
                'type': 'dict',
                'required': False,
                'options': {
                    'ip': {'type': 'str', 'required': True},
                    'mask': {'type': 'str', 'required': True},
                }
            }
        }

        super(TatlinMgmtPortModule, self).__init__(
            argument_spec=argument_spec,
            supports_check_mode=True,
        )

    def run(self):
        port = self.tatlin.get_port('mgmt')
        port_changes = self.get_port_changes(port)

        if len(port_changes) > 0:
            if not self.check_mode:
                port.update(**port_changes)
            self.exit_json(msg='Operation successful', changed=True)
        else:
            self.exit_json(msg='No changes required', changed=False)

    def get_port_changes(self, port):
        rv = {}

        for param_name in ('gateway', 'mtu', 'virtual_address'):
            new_val = self.params[param_name]
            old_val = getattr(port, param_name)

            if param_name == 'virtual_address' and new_val is not None:
                new_val = '/'.join((new_val['ip'], new_val['mask']))
                old_val = str(port.virtual_address)

            if new_val is not None and new_val != old_val:
                rv[param_name] = new_val

        if self.params['nodes'] is not None:
            nodes_changes = {}
            for node in self.params['nodes']:
                if node['name'] not in port.nodes:
                    self.fail_json(
                        msg='There is no node {node} on port {port}'.format(
                            node=node['name'], port=port.name),
                        error="Node doesn't exist",
                        changed=False,
                    )

                old_addresses = port.nodes[node['name']].addresses_str
                new_addresses = ['/'.join((address['ip'], address['mask']))
                                 for address in node['addresses']]

                need_update = len(new_addresses) != len(old_addresses) or any(
                    addr not in old_addresses for addr in new_addresses
                )

                if need_update:
                    nodes_changes[node['name']] = new_addresses

            if len(nodes_changes) > 0:
                rv['nodes'] = nodes_changes

        return rv


def main():
    TatlinMgmtPortModule()


if __name__ == "__main__":
    main()
