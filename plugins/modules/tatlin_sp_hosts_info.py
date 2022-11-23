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
module: tatlin_sp_hosts_info
short_description: Get information about hosts
description:
  - This module is intended to get information about configured
    hosts in a form of detailed inventory
  - Supports check mode
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
hosts_info:
  type: list
  elements: dict
  description: Details of the hosts
  returned: on success
  sample: [
  {
    "auth":"none",
    "name":"newhost",
    "port_type":"eth",
    "ports":["some_iqn1", "some_iqn2"],
    "tags":["tag1", "tag2"],
    "resources": ["resource1", "resource2"]
  },
  {
    "auth":null,
    "name":"another_host",
    "port_type":"fc",
    "ports":[],
    "tags":["tag3", "tag4"],
    "resources": ["resource1", "resource2"]
  }
]
"""

EXAMPLES = r"""
---
- name: Get tatlin hosts info
  yadro.tatlin_uni.tatlin_sp_hosts_info:
    connection: "{{ connection }}"
  register: result
"""


from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_module import TatlinModule


class TatlinHostsInfoModule(TatlinModule):

    def __init__(self):
        super(TatlinHostsInfoModule, self).__init__(
            supports_check_mode=True,
        )

    def run(self):
        hosts_info = [{
            'name': host.name,
            'port_type': host.port_type,
            'auth': host.auth,
            'ports': host.ports,
            'tags': host.tags,
            'resources': [r.name for r in host.get_resources()],
        } for host in self.tatlin.get_hosts()]

        self.exit_json(
            msg="Operation successful.",
            hosts_info=hosts_info,
            changed=False,
        )


def main():
    TatlinHostsInfoModule()


if __name__ == "__main__":
    main()
