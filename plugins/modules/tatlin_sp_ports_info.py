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
module: tatlin_sp_ports_info
short_description: Get information about data ports
version_added: "1.0.0"
description:
  - This module is intended to get information about data
    ports in a form of detailed inventory
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin_uni.connection_options
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
ports_info:
  type: dict
  description: Details of the data ports
  returned: on success
  sample: {
    "p00": {
      "port_type":"ip",
      "gateway":"192.168.1.1",
      "mtu":1500,
      "virtual_address":"None",
      "mac":{"sp-0":"00:00:00:00:00:00", "sp-1":"00:00:00:00:00:01"},
      "wwpn":"None",
      "nodes":{
        "sp-0":[{"ip":"192.168.1.2",
                 "mask":"24",
                 "status":"online"}],
        "sp-1":[{"ip":"192.168.1.3",
                 "mask":"24",
                 "status":"online"}]
      }
    },
    "p01": {
      "port_type":"ip",
      "gateway":"192.168.2.1",
      "mtu":1500,
      "virtual_address":"None",
      "mac":{"sp-0":"00:00:00:00:00:10", "sp-1":"00:00:00:00:00:11"},
      "wwpn":"None",
      "nodes":{
        "sp-0":[{"ip":"192.168.2.2",
                 "mask":"24",
                 "status":"online"}],
        "sp-1":[{"ip":"192.168.2.3",
                 "mask":"24",
                 "status":"online"}]
      }
    }
  }
"""

EXAMPLES = r"""
---
- name: Get ports info
  yadro.tatlin_uni.tatlin_sp_ports_info:
    connection: "{{ connection }}"
  register: result
"""


from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_module import TatlinModule


class TatlinPortInfoModule(TatlinModule):

    def __init__(self):
        super(TatlinPortInfoModule, self).__init__(
            supports_check_mode=True,
        )

    def run(self):
        all_ports = self.tatlin.get_ports()
        data_ports = [port for port in all_ports if not port.is_mgmt()]

        ports_info = dict(
            (port.name, {
                'port_type': port.type,
                'gateway': port.gateway,
                'mtu': port.mtu,
                'virtual_address': {
                    'ip': port.virtual_address.ip,
                    'mask': port.virtual_address.mask,
                } if port.virtual_address else None,
                'mac': port.mac,
                'wwpn': port.wwpn,
                'nodes': dict(
                    (node.name, [
                        {'ip': address.ip,
                         'mask': address.mask,
                         'status': address.status,
                         } for address in node.addresses
                    ]) for node in port.nodes.values())
            }) for port in data_ports
        )

        self.exit_json(
            msg="Operation successful.",
            ports_info=ports_info,
            changed=False,
        )


def main():
    TatlinPortInfoModule()


if __name__ == "__main__":
    main()
