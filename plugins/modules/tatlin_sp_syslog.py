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
module: tatlin_sp_syslog
short_description: Configure SP syslog client settings
version_added: "1.0.0"
description:
  - This module is intended to configure parameters of sending events
    to external syslog server
  - Supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin.connection_options
options:
  recipients:
    type: list
    elements: dict
    required: False
    description:
      - List of parameters of external syslog servers
      - If I(state) is C(present), at least one recipient is required.
        Also all parameters of recipients are required
    suboptions:
      address:
        type: str
        required: True
        description: Syslog server`s address in format IP or FQDN
      port:
        type: str
        required: False
        description: Syslog server`s port
      protocol:
        type: str
        required: False
        choices: [tcp, udp, tls]
        description: Transport or cryptographic protocol
      severity:
        type: str
        required: False
        choices: [critical, warning, info]
        description: Severity level of syslog messages
      facility:
        type: int
        required: False
        description: Facility level of syslog messages
      audit:
        type: bool
        required: False
        description: Enable sending audit messages
  state:
    type: str
    choices: [present, absent]
    default: present
    description:
      - C(present) sets passed syslog recipients
      - C(absent) deletes passed syslog recipients in I(recipients)
      - If no I(recipients) were passed with C(absent), all
        recipients will be removed
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
- name: Set Syslog recipients
  yadro.tatlin.tatlin_sp_syslog:
    connection: "{{ connection }}"
    recipients:
      - address: 127.0.0.1
        port: 514
        protocol: udp
        facility: 10
        severity: critical
        audit: false
      - address: example.com
        port: 601
        protocol: tls
        facility: 15
        severity: warning
        audit: true
    state: present

- name: Remove recipient by address
  yadro.tatlin.tatlin_sp_syslog:
    connection: "{{ connection }}"
    recipients:
      - address: 127.0.0.1
    state: absent

- name: Remove recipient by address and port
  yadro.tatlin.tatlin_sp_syslog:
    connection: "{{ connection }}"
    recipients:
      - address: 127.0.0.1
        port: 514
    state: absent

- name: Reset config
  yadro.tatlin.tatlin_sp_syslog:
    connection: "{{ connection }}"
    state: absent
"""


from functools import partial
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_module import TatlinModule


class TatlinSyslogModule(TatlinModule):

    def __init__(self):
        argument_spec = {
            'recipients': {
                'type': 'list',
                'elements': 'dict',
                'required': False,
                'options': {
                    'address': {'type': 'str', 'required': True},
                    'port': {'type': 'str', 'required': False},
                    'protocol': {
                        'type': 'str',
                        'choices': ['tcp', 'udp', 'tls'],
                        'required': False,
                    },
                    'severity': {
                        'type': 'str',
                        'choices': ['critical', 'warning', 'info'],
                        'required': False,
                    },
                    'facility': {'type': 'int', 'required': False},
                    'audit': {'type': 'bool', 'required': False},
                }
            },
            'state': {
                'type': 'str',
                'required': False,
                'default': 'present',
                'choices': ['present', 'absent'],
            },
        }

        super(TatlinSyslogModule, self).__init__(
            argument_spec=argument_spec,
            supports_check_mode=True,
            required_if=[
                ('state', 'present', ('recipients',)),
            ]
        )

    def run(self):
        if self.params['state'] == 'present':
            for recipient in self.params['recipients']:
                missing_params = [
                    name for name in [
                        'port', 'protocol', 'severity', 'facility', 'audit'
                    ] if recipient[name] is None
                ]

                if len(missing_params) > 0:
                    format_args = dict(
                        address=recipient['address'],
                        params=', '.join(missing_params)
                    )

                    self.fail_json(
                        msg='State is present but all of the following '
                            'recipient {address} suboptions are missing: '
                            '{params}'.format(**format_args),
                        error='Missing parameters',
                        changed=False,
                    )

        action = None
        syslog_config = self.tatlin.get_syslog_config()

        need_reset = all([
            self.params['state'] == 'absent',
            self.params['recipients'] is None,
            len(syslog_config.recipients) > 0,
        ])

        if need_reset:
            action = syslog_config.reset
        else:
            self.upper_severity()
            changes = self.get_changes(syslog_config)

            if len(changes) > 0:
                # The reason why changes are collected like not only
                # recipients can be changed is that there are potentially
                # could be other changes in future
                action = partial(
                    syslog_config.set_recipients,
                    recipients=changes['recipients']
                )

        if not action:
            self.exit_json(msg='No changes required', changed=False)

        if not self.check_mode:
            action()

        self.exit_json(msg='Operation successful', changed=True)

    def get_changes(self, syslog_config):
        rv = {}

        if self.params['state'] == 'present':

            if len(self.params['recipients']) != len(syslog_config.recipients):
                rv['recipients'] = self.params['recipients']
            else:
                need_change = False
                for new_recipient in self.params['recipients']:
                    old_recipient = syslog_config.get_recipient(
                        new_recipient['address'], new_recipient['port'],
                    )

                    if old_recipient is not None:
                        for param in (
                                'protocol',
                                'facility',
                                'severity',
                                'audit',
                        ):
                            new_value = new_recipient[param]
                            old_value = old_recipient[param]

                            if new_value != old_value:
                                need_change = True
                    else:
                        # not found
                        need_change = True

                    if need_change:
                        rv['recipients'] = self.params['recipients']
                        # If one difference was found, we have to update
                        # recipients list, so leave the cycle
                        break

        elif self.params['recipients'] is not None:  # state absent
            desired_recipients = []

            for old_recipient in syslog_config.recipients:
                ports_for_remove = [
                    r['port'] for r in self.params['recipients']
                    if r['address'] == old_recipient['address']
                ]

                need_remove = len(ports_for_remove) > 0 and any(
                    port is None or port == old_recipient['port']
                    for port in ports_for_remove
                )

                if not need_remove:
                    desired_recipients.append(old_recipient)

            if len(desired_recipients) < len(syslog_config.recipients):
                rv['recipients'] = desired_recipients

        return rv

    def upper_severity(self):
        if self.params['state'] == 'absent':
            return

        for recipient in self.params['recipients'] or []:
            recipient['severity'] = recipient['severity'].upper()


def main():
    TatlinSyslogModule()


if __name__ == "__main__":
    main()
