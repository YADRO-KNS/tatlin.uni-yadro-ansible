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
module: tatlin_sp_host_groups_info
short_description: Get information about host groups
description:
  - This module is intended to get information about configured
    host groups in a form of detailed inventory
  - Supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin.connection_options
"""

RETURN = r"""
---
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
        "tags": ["tag1", "tag2"]
      }]
    }
  ]
"""

EXAMPLES = r"""
---
- name: Get host groups info
  yadro.tatlin.tatlin_sp_host_groups_info:
    connection: "{{ connection }}"
  register: result
"""


from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_module import TatlinModule


class TatlinHostGroupsInfoModule(TatlinModule):

    def __init__(self):
        super(TatlinHostGroupsInfoModule, self).__init__(
            supports_check_mode=True,
        )

    def run(self):
        host_groups_info = [{
            'name': host_group.name,
            'tags': host_group.tags,
            'hosts': [{
                'name': host.name,
                'port_type': host.port_type,
                'auth': host.auth,
                'ports': host.ports,
                'tags': host.tags,
            } for host in host_group.hosts],
            # TODO: Resources
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
