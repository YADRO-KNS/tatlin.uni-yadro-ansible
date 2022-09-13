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
module: tatlin_sp_host_group
short_description: Create and modify host group
version_added: "1.0.0"
description:
  - This module is intended for creating new host group or change specific
    parameters for existing host group
  - Supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin.connection_options
options:
  name:
    required: True
    type: str
    description: Name of the host group
  tags:
    required: False
    type: list
    elements: str
    description: List of tags for the host group
  hosts:
    required: False
    type: list
    elements: str
    description: List of host names for including to the host group
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
- name: Create host group
  yadro.tatlin.tatlin_sp_host_group:
    connection: "{{ connection }}"
    name: testgroup
    tags:
      - tag1
      - tag2
    hosts:
      - host1
      - host2

- name: Update host group
  yadro.tatlin.tatlin_sp_host_group:
    connection: "{{ connection }}"
    name: testgroup
    tags:
      - tag2
      - tag3
    hosts:
      - host2
      - host3
"""


from functools import partial
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_module import TatlinModule


class TatlinHostGroupModule(TatlinModule):

    def __init__(self):
        argument_spec = {
            'name': {'type': 'str', 'required': True},
            'tags': {'type': 'list', 'elements': 'str', 'required': False},
            'hosts': {'type': 'list', 'elements': 'str', 'required': False},
            # TODO: Resources
        }

        super(TatlinHostGroupModule, self).__init__(
            argument_spec=argument_spec,
            supports_check_mode=True,
        )

    def run(self):
        actions = []
        host_group = self.tatlin.get_host_group(self.params['name'])

        new_hosts = self.get_new_hosts()

        if host_group is None:
            actions.append(partial(
                self.tatlin.create_host_group,
                name=self.params['name'],
                tags=self.params['tags'],
                hosts=new_hosts,
            ))
        else:
            new_tags = self.params['tags']
            old_tags = host_group.tags
            if sorted(new_tags) != sorted(old_tags):
                actions.append(partial(
                    host_group.set_tags,
                    new_tags,
                ))

            old_host_names = [host.name for host in host_group.hosts]
            new_host_names = [host.name for host in new_hosts]
            if sorted(new_host_names) != sorted(old_host_names):
                actions.append(partial(
                    host_group.set_hosts,
                    new_hosts,
                ))

        if len(actions) == 0:
            self.exit_json(msg='No changes required', changed=False)

        if not self.check_mode:
            for action in actions:
                try:
                    action()
                    self.changed = True
                except Exception as e:
                    self.fail_json(
                        msg='Operation failed',
                        error='{0}: {1}'.format(type(e).__name__, e),
                        changed=self.changed,
                    )

        self.exit_json(msg='Operation successful', changed=self.changed)

    def get_new_hosts(self):
        rv = []
        missing_hosts = []

        for host_name in self.params['hosts'] or []:
            host = self.tatlin.get_host(host_name)
            if host is None:
                missing_hosts.append(host_name)
            else:
                rv.append(host)

        if len(missing_hosts) > 0:
            self.fail_json(
                msg='Following hosts do not exist: {0}'.format(
                    ', '.join(missing_hosts)),
                error='Missing hosts',
                changed=False,
            )

        return rv


def main():
    TatlinHostGroupModule()


if __name__ == "__main__":
    main()
