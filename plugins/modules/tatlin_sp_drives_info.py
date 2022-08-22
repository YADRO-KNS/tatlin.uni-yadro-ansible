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
module: tatlin_sp_drives_info
short_description: Get information about drive groups
version_added: "1.0.0"
description:
  - This module is intended to get information about drive groups
    and physical drives in a form of detailed inventory
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
drives_info:
  type: dict
  description: Details of the drive groups
  returned: on success
  sample: [{
      "drive_capacity":"209715200",
      "drive_type":"HDD",
      "drives_available":36,
      "drives_failed":0,
      "drives_total":40,
      "drives_used":4,
      "group_name":"HDD_209.71MB",
      "space_available":"7549747200",
      "space_failed":"0",
      "space_total":"8388608000",
      "space_used":"838860800",
      "status":"Ready",
      "drives":[
        {
          "bay":"1000000001",
          "capacity":209715200,
          "model":"YADRO-shared_disk-2.5+",
          "serial_number":"0450513bb2bbd68fdc7cb9f2e38d00c0",
          "slot":"4",
          "status":"Healthy",
          "pool":{
            "available":"33554432",
            "capacity":"402653184",
            "failed":"0",
            "health":"ok",
            "id":"28118216-74eb-4ba2-8e01-be894b878de1",
            "max_capacity":4898947072,
            "max_disks_capacity":40,
            "max_spare":"1",
            "name":"testpool",
            "real_spare":"1",
            "recovery":false,
            "reserved_capacity":"201326592",
            "resource_max_size":0,
            "spare":"1",
            "status":"ready",
            "stripe_size":8192,
            "thinProvision":false,
            "used":"369098752"
          },
        },
        {
          "bay":"1000000002",
          "capacity":209715200,
          "model":"YADRO-shared_disk-2.5+",
          "pool":null,
          "serial_number":"28f1808838540d6b959ab0a1962d6443",
          "slot":"1",
          "status":"Healthy"
        }
      ],
}]
"""

EXAMPLES = r"""
---
- name: Test get tatlin drives info | Get tatlin drives info
  yadro.tatlin.tatlin_sp_drives_info:
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
        drive_groups_info = []
        drive_groups = self.tatlin.get_drive_groups()
        for group in drive_groups:
            drive_groups_info.append({
                'group_name': group.name,
                'status': group.status,
                'space_total': group.space_total,
                'space_used': group.space_used,
                'space_available': group.space_available,
                'space_failed': group.space_failed,
                'drive_type': group.type,
                'drive_capacity': group.drive_capacity,
                'drives_total': group.drives_total,
                'drives_used': group.drives_used,
                'drives_available': group.drives_available,
                'drives_failed': group.drives_failed,
                'drives': [dict(
                    model=drive.model,
                    serial_number=drive.serial_number,
                    status=drive.status,
                    capacity=drive.size,
                    pool=drive.pool,
                    bay=drive.bay,
                    slot=drive.slot,
                ) for drive in group.drives],
            })

        self.exit_json(msg="Operation successful.", drives_info=drive_groups_info)


def main():
    TatlinDrivesInfoModule()


if __name__ == "__main__":
    main()
