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
module: tatlin_sp_host_groups_info
short_description: Get information about host groups
description:
  - This module is intended to get information about configured
    host groups in a form of detailed inventory
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
host_groups_info:
  type: list
  elements: dict
  description: Details of the host groups
  returned: on success
  sample: [
    {
      "name": "testgroup",
      "tags": ["tag1", "tag2"],
      "hosts": [{
        "auth": "none",
        "name": "group_info_host",
        "port_type": "eth",
        "ports": [],
        "tags": ["tag1", "tag2"],
        "resources": ["resource1", "resource2"]
      }]
    }
  ]
"""

EXAMPLES = r"""
---
- name: Get host groups info
  yadro.tatlin_uni.tatlin_sp_host_groups_info:
    connection: "{{ connection }}"
  register: result
"""


from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_module import TatlinModule


class TatlinHostGroupsInfoModule(TatlinModule):

    def __init__(self):
        super(TatlinHostGroupsInfoModule, self).__init__(
            supports_check_mode=True,
        )

    def run(self):
        host_groups_info = [{
            'name': host_group.name,
            'tags': host_group.tags,
            'resources': [r.name for r in host_group.get_resources()],
            'hosts': [{
                'name': host.name,
                'port_type': host.port_type,
                'auth': host.auth,
                'ports': host.ports,
                'tags': host.tags,
            } for host in host_group.hosts],
        } for host_group in self.tatlin.get_host_groups()]

        self.exit_json(
            msg="Operation successful.",
            host_groups_info=host_groups_info,
            changed=False,
        )


def main():
    TatlinHostGroupsInfoModule()


if __name__ == "__main__":
    main()
