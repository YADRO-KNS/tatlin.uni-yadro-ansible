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
module: tatlin_sp_host
short_description: Create and modify host
version_added: "1.0.0"
description:
  - This module is intended for creating new host or change specific
    parameters for existing host
  - Supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin.connection_options
options:
  name:
    required: True
    type: str
    description: Name of the host
  port_type:
    required: False
    type: str
    choices: [eth, fc]
    description:
      - The port type of the host server
      - Required if new host is creating
  ports:
    required: False
    type: list
    elements: str
    description: The identifiers of the hosts` ports (wwpn or iqn)
  tags:
    required: False
    type: list
    elements: str
    description: The tags of the host
  auth:
    required: False
    type: str
    choices: ['none', 'oneway', 'mutual']
    description:
      - The type of authentication
      - Required if new host is creating and I(port_type=eth)
      - Forbidden if I(port_type=dc)
      - Forbidden to change
  username:
    required: False
    type: str
    description:
      - The name of the user for iscsi connection to Tatlin
      - Required if I(auth=oneway) or I(auth=mutual)
  password:
    required: False
    type: str
    description:
      - The password of the user for iscsi connection to Tatlin
      - Required if I(auth=oneway) or I(auth=mutual)
  mutual_username:
    required: False
    type: str
    description:
      - The name of the user for iscsi connection to host
      - Required if I(auth=mutual)
  mutual_password:
    required: False
    type: str
    description:
      - The password of the user for iscsi connection to host
      - Required if I(auth=mutual)
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
- name: Set host
  yadro.tatlin.tatlin_sp_host:
    connection: "{{ connection }}"
    name: newhost
    port_type: eth
    ports:
      - some_iqn1
      - some_iqn2
    tags:
      - tag1
      - tag2
    auth: mutual
    username: name1
    password: pass1
    mutual_username: name2
    mutual_password: name2

- name: Test host | Update tags
  yadro.tatlin.tatlin_sp_host:
    connection: "{{ connection }}"
    name: newhost
    tags:
      - tag2
      - tag3

"""


from functools import partial
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_module import TatlinModule


class TatlinHostModule(TatlinModule):

    def __init__(self):
        argument_spec = {
            'name': {'type': 'str', 'required': True},
            'port_type': {
                'type': 'str',
                'choices': ['eth', 'fc'],
                'required': False,
            },
            'ports': {'type': 'list', 'elements': 'str', 'required': False},
            'tags': {'type': 'list', 'elements': 'str', 'required': False},
            'auth': {
                'type': 'str',
                'choices': ['none', 'oneway', 'mutual'],
                'required': False,
            },
            'username': {'type': 'str', 'required': False},
            'password': {'type': 'str', 'required': False, 'no_log': True},
            'mutual_username': {'type': 'str', 'required': False},
            'mutual_password': {
                'type': 'str',
                'required': False,
                'no_log': True,
            },
        }

        required_if = [
            ('auth', 'oneway', ('username', 'password')),
            ('auth', 'mutual', (
                'username', 'password', 'mutual_username', 'mutual_password')
             ),
        ]

        super(TatlinHostModule, self).__init__(
            argument_spec=argument_spec,
            supports_check_mode=True,
            required_if=required_if,
        )

    def run(self):
        action = None
        host = self.tatlin.get_host(self.params['name'])

        if host is None:
            self.validate_params_create()
            action = partial(
                self.tatlin.create_host,
                name=self.params['name'],
                port_type=self.params['port_type'],
                auth=self.params['auth'],
                username=self.params['username'],
                password=self.params['password'],
                mutual_username=self.params['mutual_username'],
                mutual_password=self.params['mutual_password'],
                ports=self.params['ports'],
                tags=self.params['tags'],
            )
        else:
            self.validate_params_change(host)
            changes = self.get_changes(host)
            if len(changes) > 0:
                action = partial(host.update, **changes)

        if not action:
            self.exit_json(msg='No changes required', changed=False)

        if not self.check_mode:
            action()

        self.exit_json(msg='Operation successful', changed=True)

    def get_changes(self, host):
        rv = {}
        for param_name in (
            'auth',
            'username',
            'mutual_username',
            'ports',
            'tags'
        ):
            new_value = self.params[param_name]
            if new_value is None:
                continue
            old_value = getattr(host, param_name)

            if isinstance(old_value, list):
                old_value = sorted(old_value)
            if isinstance(new_value, list):
                new_value = sorted(new_value)

            if old_value != new_value:
                rv[param_name] = new_value

        if self.params['password'] is not None:
            rv['password'] = self.params['password']

        if self.params['mutual_password'] is not None:
            rv['mutual_password'] = self.params['mutual_password']

        return rv

    def validate_params_create(self):
        missing_params = []

        for param_name in ('port_type', 'auth'):
            if self.params[param_name] is None:
                missing_params.append(param_name)

        if self.params['port_type'] is None:
            self.fail_json(
                changed=False,
                error='Missing required arguments',
                msg='Missing required argument: port_type',
            )

        if self.params['port_type'] == 'eth' and self.params['auth'] is None:
            self.fail_json(
                changed=False,
                error='Missing required arguments',
                msg='auth is required with port_type == eth',
            )

        if all([
            self.params['port_type'] == 'fc',
            self.params['auth'] is not None,
        ]):
            self.fail_json(
                changed=False,
                error='Mutually exclusive parameters',
                msg='port_type == fc is mutually exclusive with auth',
            )

    def validate_params_change(self, host):
        if all([
            self.params['port_type'] is not None,
            self.params['port_type'] != host.port_type
        ]):
            self.fail_json(
                changed=False,
                error='Changing forbidden parameter',
                msg='It is prohibited to change port_type. '
                'Old value: {old_value}. '
                'New value: {new_value}'.format(
                    old_value=host.port_type,
                    new_value=self.params['port_type'],
                ),
            )


def main():
    TatlinHostModule()


if __name__ == "__main__":
    main()
