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
module: tatlin_sp_restart
short_description: Restart Storage Processor
version_added: "1.0.0"
description:
  - This module initiate restarting specified Storage Processor
  - Supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin.connection_options
options:
  node_name:
    type: str
    required: True
    description: Name of Storage Processor
notes:
  - Module doesn't wait until restart will be finished
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
- name: Restart sp-0
  yadro.tatlin.tatlin_sp_restart:
    connection: "{{ connection }}"
    node_name: sp-0
"""


from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_module import TatlinModule
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinNodeNotFoundError


class TatlinRestartModule(TatlinModule):

    def __init__(self):
        argument_spec = {
            'node_name': {'type': 'str', 'required': True},
        }

        super(TatlinRestartModule, self).__init__(
            argument_spec=argument_spec,
            supports_check_mode=True,
        )

    def _run(self):
        try:
            if not self.check_mode:
                self.tatlin_api.osmgr_service.reboot_node(
                    self.params['node_name'],
                )
        except TatlinNodeNotFoundError:
            self.fail_json(
                msg='Not found node with name {0}'.format(
                    self.params['node_name']),
                error='Node not found',
                changed=False,
            )

        self.exit_json(msg='Operation successful', changed=True)


def main():
    TatlinRestartModule().run()


if __name__ == "__main__":
    main()
