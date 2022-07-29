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
module: tatlin_sp_smtp
short_description: Configure SP SMTP settings
version_added: "1.0.0"
description:
  - This module is intended to configure sending email parameters
    via SMTP protocol
  - Supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin.connection_options
options:
  address:
    type: str
    required: False
    description: SMTP server`s address
  port:
    type: int
    required: False
    description: SMTP server`s port
  encryption:
    type: str
    required: False
    choices: [tls, 'off']
    description: Encryption type
  login:
    type: str
    required: False
    description: User's name
  password:
    type: str
    required: False
    description: User's password
  sender:
    type: str
    required: False
    description:
      - An email, which will be used as sender for sent messages
  recipients:
    type: list
    required: False
    elements: str
    description: List of emails, messages receivers
  state:
    type: str
    choices: [present, absent]
    default: present
    description:
      - C(present) sets passed SMTP configuration
      - C(absent) deletes passed SMTP servers in I(recipients)
      - If no I(recipients) were passed with C(absent), all
        configuration will be removed
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
- name: Set SMTP config
  yadro.tatlin.tatlin_sp_smtp:
    connection: "{{ connection }}"
    address: 127.0.0.1
    port: 25
    login: admin
    password: ***REMOVED***
    sender: smtp@example.com
    state: present
    recipients:
      - first@recipient.com
      - second@recipient.com

- name: Add recipients
  yadro.tatlin.tatlin_sp_smtp:
    connection: "{{ connection }}"
    recipients:
      - first@recipient.com
      - second@recipient.com
      - third@recipient.com

- name: Remove recipient
  yadro.tatlin.tatlin_sp_smtp:
    connection: "{{ connection }}"
    recipients:
      - second@recipient.com
    state: absent

- name: Clear config
  yadro.tatlin.tatlin_sp_smtp:
    connection: "{{ connection }}"
    state: absent
"""


from functools import partial
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_module import TatlinModule


class TatlinSmtpModule(TatlinModule):

    def __init__(self):
        argument_spec = {
            'address': {'type': 'str', 'required': False},
            'port': {'type': 'int', 'required': False},
            'encryption': {
                'type': 'str',
                'choices': ['tls', 'off'],
                'required': False,
            },
            'login': {'type': 'str', 'required': False},
            'password': {'type': 'str', 'no_log': True, 'required': False},
            'sender': {'type': 'str', 'required': False},
            'recipients': {
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

        super(TatlinSmtpModule, self).__init__(
            argument_spec=argument_spec,
            supports_check_mode=True,
        )

    def _run(self):
        action = None
        smtp_config = self.tatlin_api.notification_service.get_smtp_config()
        self.check_parameters(smtp_config)

        # Consider that if host address is not empty, SMTP is configured
        is_configured = smtp_config.address is not None

        changes = self.get_changes(smtp_config)
        if len(changes) > 0:
            action = partial(smtp_config.update, **changes)
        elif self.params['state'] == 'absent' \
                and self.params['recipients'] is None \
                and is_configured:
            action = smtp_config.reset

        if not action:
            self.exit_json(msg='No changes required', changed=False)

        if not self.check_mode:
            action()

        self.exit_json(msg='Operation successful', changed=True)

    def check_parameters(self, smtp_config):

        if self.params['state'] == 'present':
            missing_params = []

            for param_name in ('address', 'port', 'sender'):
                new_value = self.params[param_name]
                old_value = getattr(smtp_config, param_name)

                if new_value is None and old_value is None:
                    missing_params.append(param_name)

            if len(missing_params) > 0:
                self.fail_json(
                    msg='It is forbidden to configure SMTP settings without '
                        'required parameters: {0}'.format(missing_params),
                    error='Missing parameters',
                    changed=False,
                )

            if self.params['login'] and not self.params['password']:
                self.fail_json(
                    msg='Missing pararmeter password when login was passed',
                    error='Missing parameter',
                    changed=False,
                )

        elif self.params['state'] == 'absent':
            forbidden_params = []

            for param_name in (
                'address',
                'port',
                'sender',
                'login',
                'password',
            ):
                if self.params[param_name] is not None:
                    forbidden_params.append(param_name)

            if len(forbidden_params) > 0:
                self.fail_json(
                    msg='State absent is mutually exclusive with '
                        'parameters: {0}'.format(', '.join(forbidden_params)),
                    error='Mutually exclusive parameters',
                    changed=False,
                )

    def get_changes(self, smtp_config):
        rv = {}

        if self.params['state'] == 'present':
            for param_name in (
                    'address',
                    'port',
                    'encryption',
                    'login',
                    'sender',
            ):
                new_value = self.params[param_name]
                old_value = getattr(smtp_config, param_name)

                if new_value is not None and new_value != old_value:
                    rv[param_name] = new_value

            if self.params['password'] is not None:
                rv['password'] = self.params['password']

            new_recipients = self.params['recipients']
            old_recipients = smtp_config.recipients
            if new_recipients is not None and \
                    not same_lists(new_recipients, old_recipients):
                rv['recipients'] = new_recipients

        elif self.params['recipients'] is not None:  # state is absent
            desired_recipients = [
                rec for rec in smtp_config.recipients
                if rec not in self.params['recipients']
            ]

            if not same_lists(desired_recipients, smtp_config.recipients):
                rv['recipients'] = desired_recipients

        return rv


def same_lists(list1, list2):
    return sorted(list1) == sorted(list2)


def main():
    TatlinSmtpModule().run()


if __name__ == "__main__":
    main()
