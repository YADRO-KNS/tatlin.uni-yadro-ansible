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
module: tatlin_sp_resources_info
short_description: Get information about configured resources
description:
  - This module is intended to get information about configured
    storage resources in a form of detailed inventory
  - Supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin.connection_options
notes:
  - All capacity values are returned in bytes size
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
resources_info:
  type: list
  elements: dict
  description: Details of the pools
  returned: on success
  sample: [{
    "name": "example_resource_block",
    "type": "block",
    "pool": "example_pool",
    "status": "online",
    "capacity_total": 104857600,
    "capacity_used": 10485760,
    "read_cache": True,
    "write_cache": False,
    "warning_threshold": 70,
    "ports": ["p00", "p01"],
    "hosts": ["example_host1", "example_host2"],
    "host_groups": ["example_host_group1", "example_host_group2"],
    "subnets": [],
    "users": [],
    "user_groups": []
  },
  {
    "name": "example_resource_file",
    "type": "nfs",
    "pool": "example_pool",
    "status": "online",
    "capacity_total": 104857600,
    "capacity_used": 10485760,
    "read_cache": True,
    "write_cache": False,
    "warning_threshold": None,
    "ports": ["p00", "p01"],
    "hosts": [],
    "host_groups": [],
    "subnets": ["example_subnet1", "example_subnet2"],
    "users": [
      {"name": "example_user1",
       "permissions": "rw"},
      {"name": "example_user2",
       "permissions": "r"}
    ],
    "user_groups": [
      {"name": "example_user_group1",
       "permissions": "r"},
      {"name": "example_user_group2",
       "permissions": "rw"}
    ]
  }]
"""

EXAMPLES = r"""
---
- name: Get resources info
  yadro.tatlin.tatlin_sp_resources_info:
    connection: "{{ connection }}"
  register: result
"""


from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_module import TatlinModule


class TatlinResourcesInfoModule(TatlinModule):

    def __init__(self):
        super(TatlinResourcesInfoModule, self).__init__(
            supports_check_mode=True,
        )

    def run(self):
        resources_info = [{
            'name': resource.name,
            'type': resource.type,
            'pool': resource.pool.name,
            'status': resource.status,
            'capacity_total': resource.capacity_total,
            'capacity_used': resource.capacity_used,
            'read_cache': resource.read_cache,
            'write_cache': resource.write_cache,
            'warning_threshold': resource.warning_threshold,
            'ports': [port.name for port in resource.ports],
            'hosts': [host.name for host in resource.hosts],
            'host_groups': [group.name for group in resource.host_groups],
            'subnets': [subnet.name for subnet in resource.subnets],
            'users': [{
                'name': user.name,
                'permissions': resource.get_user_permissions(user),
            } for user in resource.users],
            'user_groups': [{
                'name': group.name,
                'permissions': resource.get_user_group_permissions(group),
            } for group in resource.user_groups],
        } for resource in self.tatlin.get_resources()]

        self.exit_json(
            msg="Operation successful.",
            resources_info=resources_info,
            changed=False,
        )


def main():
    TatlinResourcesInfoModule()


if __name__ == "__main__":
    main()
