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
    "resources": [],
    "resources_count": 0,
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
    "resources": [
     {"available_ports_number": 8,
      "blockSize": "4kn",
      "cached": "true",
      "id": "c66dbc61-6e79-425b-b2ae-e396fd06ee68",
      "lbaFormat": "4kn",
      "lun_id": "1",
      "maxModifySize": 353370112,
      "min_limit_bw": 10485760,
      "min_limit_iops": 10,
      "name": "rsrc",
      "overhead": 15728640,
      "poolId": "4eb5ca1d-2d7f-4c1a-8e81-052cff6cfecd",
      "ptyId": "c66dbc61-6e79-425b-b2ae-e396fd06ee68",
      "rCacheMode": "enabled",
      "replication": {
        "is_enabled": false
      },
      "size": 1048576,
      "stat": {
        "dedup_count": 0,
        "mapped_blocks": 0,
        "reduction_ratio": 0,
        "used_capacity": 1048576
      },
      "status": "ready",
      "type": "block",
      "volume_id": "pty-vol-c66dbc61-6e79-425b-b2ae-e396fd06ee68",
      "volume_path": "/dev/mapper/dmc-fd968fd3-94fe-4896-b642-52bece3ca37b",
      "wCacheMode": "enabled",
      "wwid": "naa.61452901305803104000800000000001"}
    ],
    "resources_count": 1,
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


class TatlinDrivesInfoModule(TatlinModule):

    def __init__(self):
        super(TatlinDrivesInfoModule, self).__init__(
            supports_check_mode=True,
        )

    def run(self):
        pools_info = [{
            'name': pool.name,
            'provision': pool.provision,
            'status': pool.status,
            'resources_count': len(pool.resources),
            'capacity_total': pool.capacity_total,
            'capacity_available': pool.capacity_available,
            'capacity_used': pool.capacity_used,
            'capacity_failed': pool.capacity_failed,
            'protection': pool.protection,
            'spare_count': pool.spare_count,
            'stripe_size': pool.stripe_size,
            'warning_threshold': pool.warning_threshold,
            'critical_threshold': pool.critical_threshold,
            'resources': pool.resources,
        } for pool in self.tatlin.get_all_pools()]

        self.exit_json(msg="Operation successful.", pools_info=pools_info)


def main():
    TatlinDrivesInfoModule()


if __name__ == "__main__":
    main()
