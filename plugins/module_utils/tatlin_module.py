# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    from typing import Dict, List, Sequence
except ImportError:
    Dict = List = Sequence = None

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.tatlin_client import TatlinClient


class TatlinModule(AnsibleModule):

    def __init__(
        self,
        argument_spec=None,
        supports_check_mode=False,
        required_if=None,
        mutually_exclusive=None,
    ):
        # type: (Dict, bool, Sequence, List) -> None
        _argument_spec = {
            "connection": {
                "required": True,
                "type": "dict",
                "options": {
                    "base_url": {"required": True, "type": "str"},
                    "username": {"required": False, "type": "str"},
                    "password": {
                        "required": False,
                        "type": "str",
                        "no_log": True,
                    },
                    "validate_certs": {
                        "required": False,
                        "type": "bool",
                        "default": True,
                    },
                    "login_path": {
                        "required": False,
                        "type": "str",
                        "default": "auth/login",
                    },
                    "timeout": {
                        "required": False,
                        "type": "int",
                        "default": 60,
                    },
                }
            },
        }
        if argument_spec and isinstance(argument_spec, dict):
            _argument_spec.update(argument_spec)

        super(TatlinModule, self).__init__(
            argument_spec=_argument_spec,
            supports_check_mode=supports_check_mode,
            required_if=required_if,
            mutually_exclusive=mutually_exclusive,
        )

        self.tatlin_api = None  # type: TatlinClient

    def run(self):  # type: () -> None
        connection = self.params["connection"]

        self.tatlin_api = TatlinClient(
            base_url=connection['base_url'],
            username=connection['username'],
            password=connection['password'],
            validate_certs=connection['validate_certs'],
            login_path=connection['login_path'],
            timeout=connection['timeout'],
        )

        try:
            self.tatlin_api.authorize()
            self._run()
        except Exception as e:
            self.fail_json(
                msg='Operation failed',
                error='{0}: {1}'.format(type(e).__name__, e),
            )

    def _run(self):  # type: () -> None
        raise NotImplementedError('Method not implemented!')
