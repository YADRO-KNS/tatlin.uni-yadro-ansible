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
module: tatlin_sp_user
short_description: Configure SP user
version_added: "1.0.0"
description:
  - Purpose of this module is to create/change local user's attributes
  - This module supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin.connection_options
options:
  name:
    required: True
    type: str
    description: The name of the user
  password:
    type: str
    description:
      - The password of the user.
      - Required when creating a new user.
  groups:
    type: list
    elements: str
    description:
      - The groups of the user that restrict user permissions.
      - Required when creating a new user
  enabled:
    type: bool
    description:
      - Indication of whether a user is enabled
      - Required when creating a new user
      - C(true) if the user is enabled, the user can log in
      - C(false) if the user is disabled, the user cannot log in
  state:
    type: str
    choices: [present, absent]
    default: present
    description:
      - C(present) creates a new user if I(name) does not exists.
        Otherwise change user parameters
      - C(absent) deletes an existing user
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
- name: Create TestUser
  yadro.tatlin.tatlin_sp_user:
    connection: "{{ connection }}"
    name: "TestUser"
    password: "TestPassword"
    groups:
      - data
      - monitor
    enabled: true
    state: "present"

- name: Modify TestUser
  yadro.tatlin.tatlin_sp_user:
    connection: "{{ connection }}"
    name: "TestUser"
    enabled: false
    groups:
      monitor

- name: Delete TestUser
  yadro.tatlin.tatlin_sp_user:
    connection: "{{ connection }}"
    name: "TestUser"
    state: "absent"
"""


from functools import partial
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_module import TatlinModule


class TatlinUserModule(TatlinModule):

    def __init__(self):
        argument_spec = {
            'name': {'type': 'str', 'required': True},
            'password': {'type': 'str', 'required': False, 'no_log': True},
            'groups': {'type': 'list', 'elements': 'str', 'required': False},
            'enabled': {'type': 'bool', 'required': False},
            'state': {
                'type': 'str',
                'required': False,
                'default': 'present',
                'choices': ['present', 'absent']
            },
        }

        super(TatlinUserModule, self).__init__(
            argument_spec=argument_spec,
            supports_check_mode=True,
        )

    def _run(self):
        action = None
        user = self.tatlin.auth_service.get_user(self.params['name'])
        user_exists = user is not None

        if self.params['state'] == 'present':
            if user_exists:  # update
                upd_params = {}
                if self.params['password'] is not None:
                    upd_params['password'] = self.params['password']

                if self.params['groups'] is not None:
                    fact_groups = set(group.name for group in user.groups)
                    required_groups = set(self.params['groups'])
                    if fact_groups != required_groups:
                        upd_params['groups'] = self.params['groups']

                if self.params['enabled'] is not None \
                        and self.params['enabled'] != user.enabled:
                    upd_params['enabled'] = self.params['enabled']

                if len(upd_params) > 0:
                    action = partial(user.update, **upd_params)

            else:  # creation
                self._check_creating_params()
                action = partial(
                    self.tatlin.auth_service.create_user,
                    name=self.params['name'],
                    password=self.params['password'],
                    groups=self.params['groups'],
                    enabled=self.params['enabled'],
                )
        else:
            if user_exists:
                action = user.delete

        if not action:
            self.exit_json(msg='No changes required', changed=False)

        if not self.check_mode:
            action()

        self.exit_json(msg='Operation successful', changed=True)

    def _check_creating_params(self):
        missed_args = []
        for arg in ['password', 'groups', 'enabled']:
            if self.params[arg] is None:
                missed_args.append(arg)

        if missed_args:
            self.fail_json(
                msg='Cannot create new account.',
                error='Fields required: {0}.'.format(', '.join(missed_args)),
                changed=False
            )


def main():
    TatlinUserModule().run()


if __name__ == "__main__":
    main()
