# -*- coding: utf-8 -*-

# YADRO Tatlin Unified Ansible Collection
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
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.tatlin_client import TatlinClient
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.exception import TatlinAuthorizationError


class TatlinModule(AnsibleModule):

    def __init__(
        self,
        argument_spec=None,
        supports_check_mode=False,
        required_if=None,
        required_one_of=None,
        mutually_exclusive=None,
    ):
        # type: (Dict, bool, Sequence, Sequence, Sequence) -> None
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
            required_one_of=required_one_of,
            mutually_exclusive=mutually_exclusive,
        )

        connection = self.params['connection']

        self.tatlin = TatlinClient(
            base_url=connection['base_url'],
            username=connection['username'],
            password=connection['password'],
            validate_certs=connection['validate_certs'],
            timeout=connection['timeout'],
        )

        self.changed = False

        try:
            self.tatlin.authorize()
            self.run()
        except TatlinAuthorizationError as e:
            self.fail_json(
                msg='Authorization failed',
                error='{0}: {1}'.format(type(e).__name__, e),
            )
        except Exception as e:
            self.fail_json(
                msg='Operation failed',
                error='{0}: {1}'.format(type(e).__name__, e),
            )

    def run(self):  # type: () -> None
        raise NotImplementedError('Method not implemented!')

    def exit_json(self, **kwargs):
        self._logout()
        super(TatlinModule, self).exit_json(**kwargs)

    def fail_json(self, **kwargs):
        self._logout()
        super(TatlinModule, self).fail_json(**kwargs)

    def _logout(self):
        try:
            self.tatlin.logout()
        except Exception as e:
            self.warn(
                'Logout failed. {0}: {1}'.format(type(e).__name__, e)
            )
