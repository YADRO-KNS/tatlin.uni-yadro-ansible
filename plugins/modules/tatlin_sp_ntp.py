#!/usr/bin/python
# -*- coding: utf-8 -*-

# YADRO Tatlin Unified Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r"""
---
module: tatlin_sp_ntp
short_description: Configure SP NTP client settings
version_added: "1.0.0"
description:
  - This module is intended to configure IP addresses and FQDNs of NTP servers
    which will be used by Tatlin for time synchronization
  - Supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin_uni.connection_options
options:
  servers:
    required: False
    type: list
    elements: str
    description:
      - NTP servers` address list
      - Required if I(state) is C(present)
  state:
    type: str
    choices: [present, absent]
    default: present
    description:
      - C(present) sets passed NTP servers' addresses
      - C(absent) deletes passed NTP servers' addresses
      - If no addresses were passed with C(absent), all
        addresses will be removed
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
- name: Set ntp servers
  yadro.tatlin_uni.tatlin_sp_ntp:
    connection: "{{ connection }}"
    servers:
      - 192.168.1.11
      - example.com
      - 127.0.0.1

- name: Remove ntp server
  yadro.tatlin_uni.tatlin_sp_ntp:
    connection: "{{ connection }}"
    servers:
      - 127.0.0.1
    state: absent

- name: Remove all ntp servers
  yadro.tatlin_uni.tatlin_sp_ntp:
    connection: "{{ connection }}"
    state: absent
"""


from functools import partial
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_module import TatlinModule


class TatlinNtpModule(TatlinModule):

    def __init__(self):
        argument_spec = {
            'servers': {'type': 'list', 'elements': 'str', 'required': False},
            'state': {
                'type': 'str',
                'required': False,
                'default': 'present',
                'choices': ['present', 'absent'],
            },
        }

        super(TatlinNtpModule, self).__init__(
            argument_spec=argument_spec,
            supports_check_mode=True,
            required_if=[('state', 'present', ('servers',))],
        )

    def run(self):
        action = None
        ntp_config = self.tatlin.get_ntp_config()

        if self.params['state'] == 'present':
            if not same_servers(self.params['servers'], ntp_config.servers):
                action = partial(
                    ntp_config.set_servers,
                    self.params['servers'],
                )
        else:
            if self.params['servers'] is not None:
                desired_servers = [s for s in ntp_config.servers
                                   if s not in self.params['servers']]

                if not same_servers(desired_servers, ntp_config.servers):
                    action = partial(
                        ntp_config.set_servers,
                        desired_servers,
                    )
            elif len(ntp_config.servers) > 0:
                action = ntp_config.reset_servers

        if not action:
            self.exit_json(msg='No changes required', changed=False)

        if not self.check_mode:
            action()

        self.exit_json(msg='Operation successful', changed=True)


def same_servers(servers1, servers2):
    return sorted(servers1) == sorted(servers2)


def main():
    TatlinNtpModule()


if __name__ == "__main__":
    main()
