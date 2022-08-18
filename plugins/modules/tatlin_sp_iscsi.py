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
module: tatlin_sp_iscsi
short_description: Manage iSCSI credentials
version_added: "1.0.0"
description:
  - This module is intended to manage credentials,
    which are used for ISCSI authorization
  - Supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin.connection_options
options:
  auth:
    required: True
    type: str
    choices: ['none', 'oneway', 'mutual']
    description: Discovery auth type
  username:
    required: False
    type: str
    description:
      - ISCSI discovery CHAP username
      - Required if I(auth) is C(oneway) or C(mutual)
  password:
    required: False
    type: str
    description:
      - ISCSI discovery CHAP password
      - Required if I(auth) is C(oneway) or C(mutual)
  mutual_username:
    required: False
    type: str
    description:
      - ISCSI discovery CHAP mutual username
      - Required if I(auth) is C(mutual)
  mutual_password:
    required: False
    type: str
    description:
      - ISCSI discovery CHAP mutual password
      - Required if I(auth) is C(mutual)
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
- name: Set none auth type
  yadro.tatlin.tatlin_sp_iscsi:
    connection: "{{ connection }}"
    auth: none

- name: Set oneway auth type
  yadro.tatlin.tatlin_sp_iscsi:
    connection: "{{ connection }}"
    auth: oneway
    username: user1
    password: user1

- name: Set mutual auth type
  yadro.tatlin.tatlin_sp_iscsi:
    connection: "{{ connection }}"
    auth: mutual
    username: user1
    password: user1
    mutual_username: user2
    mutual_password: user2
"""


from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_module import TatlinModule


class TatlinIscsiModule(TatlinModule):

    def __init__(self):
        argument_spec = {
            'auth': {
                'type': 'str',
                'choices': ['none', 'oneway', 'mutual'],
                'required': True,
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

        super(TatlinIscsiModule, self).__init__(
            argument_spec=argument_spec,
            supports_check_mode=True,
            required_if=required_if,
        )

    def run(self):
        if not self.check_mode:
            self.tatlin.personalities_service.set_iscsi_auth(
                auth=self.params['auth'],
                username=self.params['username'],
                password=self.params['password'],
                mutual_username=self.params['mutual_username'],
                mutual_password=self.params['mutual_password'],
            )

        self.exit_json(msg='Operation successful', changed=True)


def main():
    TatlinIscsiModule()


if __name__ == "__main__":
    main()
