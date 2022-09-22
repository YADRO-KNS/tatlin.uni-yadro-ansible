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
module: tatlin_sp_subnet
short_description: Create, modify or remove a subnet
version_added: "1.0.0"
description:
  - This module is intended to configure and remove subnets
  - Supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin.connection_options
options:
  name:
    required: True
    type: str
    description: The name of the subnet
  ip_start:
    required: False
    type: str
    description:
      - First ip in range of ips
      - Required if new subnet is creating
  ip_end:
    required: False
    type: str
    description:
      - Last ip in range of ips
      - Required if new subnet is creating
  state:
    type: str
    choices: [present, absent]
    default: present
    description:
      - C(present) create a new subnet or change an existing subnet
      - C(absent) removes an existing subnet
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
- name: Create new subnet
  yadro.tatlin.tatlin_sp_subnet:
    connection: "{{ connection }}"
    name: example_subnet
    ip_start: '192.168.0.2'
    ip_end: '192.168.0.3'
    state: present

- name: Change subnet
  yadro.tatlin.tatlin_sp_subnet:
    connection: "{{ connection }}"
    name: example_subnet
    ip_start: '192.168.0.2'
    ip_end: '192.168.0.3'

- name: Remove subnet
  yadro.tatlin.tatlin_sp_subnet:
    connection: "{{ connection }}"
    name: example_subnet
    state: absent
"""


from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_module import TatlinModule


class TatlinSubnetModule(TatlinModule):

    def __init__(self):
        argument_spec = {
            'name': {'type': 'str', 'required': True},
            'ip_start': {'type': 'str', 'required': False},
            'ip_end': {'type': 'str', 'required': False},
            'state': {
                'type': 'str',
                'required': False,
                'default': 'present',
                'choices': ['present', 'absent'],
            },
        }

        super(TatlinSubnetModule, self).__init__(
            argument_spec=argument_spec,
            supports_check_mode=True,
            required_if=[('state', 'present', ('ip_start', 'ip_end'))],
        )

    def run(self):
        task = None
        subnet = self.tatlin.get_subnet(self.params['name'])

        if self.params['state'] == 'present':
            if subnet is None:
                if not self.check_mode:
                    task = self.tatlin.create_subnet(
                        name=self.params['name'],
                        ip_start=self.params['ip_start'],
                        ip_end=self.params['ip_end'],
                    )
                self.changed = True
            else:
                new_ip_start = self.params['ip_start']
                new_ip_end = self.params['ip_end']
                old_ip_start = subnet.ip_start
                old_ip_end = subnet.ip_end

                if new_ip_start != old_ip_start or new_ip_end != old_ip_end:
                    if not self.check_mode:
                        task = subnet.update(ip_start=new_ip_start, ip_end=new_ip_end)
                    self.changed = True
        else:
            if subnet is not None:
                if not self.check_mode:
                    task = subnet.remove()
                self.changed = True

        if task is not None:
            try:
                task.wait_until_complete()
            except Exception as e:
                self.fail_json(
                    changed=True,
                    error=type(e).__name__,
                    msg=str(e),
                )

        if self.changed:
            result_msg = 'Operation successful'
        else:
            result_msg = 'No changes required'

        self.exit_json(
            msg=result_msg,
            changed=self.changed,
        )


def main():
    TatlinSubnetModule()


if __name__ == "__main__":
    main()
