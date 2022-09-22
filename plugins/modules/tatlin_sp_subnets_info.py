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
module: tatlin_sp_subnets_info
short_description: Get information about subnets
version_added: "1.0.0"
description:
  - This module is intended to get information about
    subnets in a form of detailed inventory
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin.connection_options
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
subnets_info:
  type: list
  elements: dict
  description: Details of subnets
  returned: on success
  sample: [
    {"name": "example_subnet1",
     "ip_range": "192.168.0.11-192.168.0.20"},
    {"name": "example_subnet2",
     "ip_range": "192.168.0.21-192.168.0.30"}
  ]
"""

EXAMPLES = r"""
---
- name: Get subnets info
  yadro.tatlin.tatlin_sp_subnets_info:
    connection: "{{ connection }}"
  register: result
"""


from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_module import TatlinModule


class TatlinSubnetsInfoModule(TatlinModule):

    def __init__(self):
        super(TatlinSubnetsInfoModule, self).__init__(
            supports_check_mode=True,
        )

    def run(self):
        subnets_info = [{
            'name': subnet.name,
            'ip_range': '{0}-{1}'.format(subnet.ip_start, subnet.ip_end)
            # TODO: Add resources
        } for subnet in self.tatlin.get_subnets()]

        self.exit_json(
            msg="Operation successful.",
            subnets_info=subnets_info,
            changed=False,
        )


def main():
    TatlinSubnetsInfoModule()


if __name__ == "__main__":
    main()
