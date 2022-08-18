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
module: tatlin_sp_group
short_description: Configure SP user group
version_added: "1.0.0"
description:
  - Purpose of this module is to create/change user groups
  - This module supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin.connection_options
options:
  name:
    required: True
    type: str
    description: The name of the user group
  parent_groups:
    required: False
    type: list
    elements: str
    description: Groups that group I(name) will belong to
  comment:
    required: False
    type: str
    description: Additional information about group
  state:
    type: str
    choices: [present, absent]
    default: present
    description:
      - C(present) creates a new group if I(name) does not exists.
        Otherwise change group parameters
      - C(absent) deletes an existing group
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
- name: Create TestGroup
  yadro.tatlin.tatlin_sp_group:
    connection: "{{ connection }}"
    name: "TestGroup"
    parent_groups:
      - data
      - monitor
    comment: Testing group
    state: "present"

- name: Modify TestGroup
  yadro.tatlin.tatlin_sp_group:
    connection: "{{ connection }}"
    name: "TestGroup"
    parent_groups:
      - admin
    comment: Testing admin group

- name: Delete TestGroup
  yadro.tatlin.tatlin_sp_group:
    connection: "{{ connection }}"
    name: "TestGroup"
    state: "absent"
"""


from functools import partial
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_module import TatlinModule


class TatlinUserGroupModule(TatlinModule):

    def __init__(self):
        argument_spec = {
            'name': {'type': 'str', 'required': True},
            'comment': {'type': 'str', 'required': False},
            'parent_groups': {
                'type': 'list',
                'elements': 'str',
                'required': False,
            },
            'state': {
                'type': 'str',
                'required': False,
                'default': 'present',
                'choices': ['present', 'absent'],
            },
        }

        super(TatlinUserGroupModule, self).__init__(
            argument_spec=argument_spec,
            supports_check_mode=True,
        )

    def run(self):
        action = None
        group = self.tatlin.get_user_group(
            self.params['name'],
        )
        group_exists = group is not None

        if self.params['state'] == 'present':
            if group_exists:  # update
                upd_params = {}
                if self.params['parent_groups'] is not None:
                    fact_parents = set(g.name for g in group.parent_groups)
                    required_parents = set(self.params['parent_groups'])
                    if fact_parents != required_parents:
                        upd_params['parent_groups'] = list(required_parents)

                if self.params['comment'] is not None \
                        and self.params['comment'] != group.comment:
                    upd_params['comment'] = self.params['comment']

                if len(upd_params) > 0:
                    action = partial(group.update, **upd_params)

            else:  # creation
                action = partial(
                    self.tatlin.create_user_group,
                    name=self.params['name'],
                    parent_groups=self.params['parent_groups'],
                    comment=self.params['comment'],
                )
        else:
            if group_exists:
                action = group.delete

        if not action:
            self.exit_json(msg='No changes required', changed=False)

        if not self.check_mode:
            action()

        self.exit_json(msg='Operation successful', changed=True)


def main():
    TatlinUserGroupModule()


if __name__ == "__main__":
    main()
