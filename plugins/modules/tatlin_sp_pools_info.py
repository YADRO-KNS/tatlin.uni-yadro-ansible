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
module: tatlin_sp_pools_info
short_description: Get information about configured pools.
description:
  - This module is intended to get information about configured
    pools in a form of detailed inventory
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
pools_info:
  type: list
  elements: dict
  description: Details of the pools
  returned: on success
  sample: [
  {
    "capacity_available": 301989888,
    "capacity_failed": 0,
    "capacity_total": 301989888,
    "capacity_used": 0,
    "critical_threshold": 66,
    "name": "testpool1",
    "protection": "1+1",
    "provision": "thin",
    "resources": [
    {"name": "example_resource",
     "type": "block",
     "status": "online",
     "capacity_total": 201326592,
     "capacity_used": 201326592,
     "read_cache": true,
     "write_cache": true,
     "warning_threshold": 69,
     "ports": ["p00", "p01"],
     "hosts": ["host_example1", "host_example2"],
     "host_groups": ["group_example1", "group_example2"]}
     ],
    "resources_count": 1,
    "spare_count": 1,
    "status": "ready",
    "warning_threshold": 65},
  {
    "capacity_available": 352321536,
    "capacity_failed": 0,
    "capacity_total": 369098752,
    "capacity_used": 16777216,
    "critical_threshold": null,
    "name": "testpool2",
    "protection": "1+1",
    "provision": "thick",
    "resources": [],
    "resources_count": 0,
    "spare_count": 1,
    "status": "ready",
    "warning_threshold": null
  }
]
"""

EXAMPLES = r"""
---
- name: Get tatlin pools info
  yadro.tatlin.tatlin_sp_pools_info:
    connection: "{{ connection }}"
  register: result
"""


from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_module import TatlinModule


class TatlinPoolsInfoModule(TatlinModule):

    def __init__(self):
        super(TatlinPoolsInfoModule, self).__init__(
            supports_check_mode=True,
        )

    def run(self):
        pools_info = [{
            'name': pool.name,
            'provision': pool.provision,
            'status': pool.status,
            'resources_count': len(pool.get_resources()),
            'capacity_total': pool.capacity_total,
            'capacity_available': pool.capacity_available,
            'capacity_used': pool.capacity_used,
            'capacity_failed': pool.capacity_failed,
            'protection': pool.protection,
            'spare_count': pool.spare_count,
            'stripe_size': pool.stripe_size,
            'warning_threshold': pool.warning_threshold,
            'critical_threshold': pool.critical_threshold,
            'resources': [{
                'name': resource.name,
                'type': resource.type,
                'status': resource.status,
                'size_format': resource.size_format,
                'capacity_total': resource.capacity_total,
                'capacity_used': resource.capacity_used,
                'read_cache': resource.read_cache,
                'write_cache': resource.write_cache,
                'warning_threshold': resource.warning_threshold,
                'ports': [port.name for port in resource.ports],
                'hosts': [host.name for host in resource.hosts],
                'host_groups': [group.name for group in resource.host_groups],
                'users': [user.name for user in resource.users],
                'user_groups': [group.name for group in resource.user_groups]
            } for resource in pool.get_resources()],
        } for pool in self.tatlin.get_pools()]

        self.exit_json(
            msg="Operation successful.",
            pools_info=pools_info,
            changed=False,
        )


def main():
    TatlinPoolsInfoModule()


if __name__ == "__main__":
    main()
