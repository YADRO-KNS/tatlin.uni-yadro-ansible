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
module: tatlin_sp_ldap
short_description: Configure SP LDAP client settings.
version_added: "1.0.0"
description:
  - This module is intended to configure ldap settings
    for Storage Processor.
  - Supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin.connection_options
options:
  host:
    required: False
    type: str
    description: Ldap server's address
  port:
    required: False
    type: str
    description: Ldap server's port
  lookup_user:
    required: False
    type: str
    description: Name of lookup user
  lookup_password:
    required: False
    type: str
    description:
      - Password for lookup user
      - Required if (I)state is (C)present
  base_dn:
    required: False
    type: str
    description: Ldap server's base dn for search
  search_filter:
    required: False
    type: str
    description: Filter in RFC 4515 format
  encryption:
    required: False
    type: str
    choices: [ssl, tls, 'off']
    description:
      - Encryption mode
      - If ldap is encrypted ((C)ssl or (C)tls), certificate must be passed.
        If ldap was already configured as encrypted and one or several fields
        are updated (for example (I)search_filter) (I)crt_path or
        (I)crt_content must be passed. Otherwise an operation will be failed
  crt_path:
    required: False
    type: str
    description:
      - Path to ldap server's certificate
      - Required if (I)encryption is (C)ssl or (C)tls
      - Mutually exclusive with (I)crt_content
  crt_content:
    required: False
    type: str
    description:
      - Content of ldap server's certificate
      - Required if (I)encryption is (C)ssl or (C)tls
      - Mutually exclusive with (I)crt_path
  user_attribute:
    required: False
    type: str
    description:
     - User attribute for search
     - Prohibited if (I)type is (C)ad
  group_attribute:
    required: False
    type: str
    description:
      - Group attribute for search
      - Prohibited if (I)type is (C)ad
  type:
    required: False
    type: str
    choices: [ad, custom]
    description: Ldap server's type
  state:
    required: False
    type: str
    choices: [present, absent]
    default: present
    description: Ldap server's type
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
- name: Add ldap config
  yadro.tatlin.tatlin_sp_ldap:
    connection: "{{ connection }}"
    host: "{{ ldap_host }}"
    port: 389
    lookup_user: cn=admin,dc=example,dc=com
    lookup_password: password
    base_dn: dc=example,dc=com
    search_filter: "(memberof=cn=Users,dc=example,dc=com)"
    encryption: off
    user_attribute: cn
    group_attribute: cn
    type: custom

- name: Change search filter
  yadro.tatlin.tatlin_sp_ldap:
    connection: "{{ connection }}"
    lookup_password: password
    search_filter: (uid=*)

- name: Enable tls encryption
  yadro.tatlin.tatlin_sp_ldap:
    connection: "{{ connection }}"
    lookup_password: password
    encryption: tls
    port: 389
    crt_path: /path/to/certificate.pem

- name: Add AD config with ssl encryption
  yadro.tatlin.tatlin_sp_ldap:
    connection: "{{ connection }}"
    host: "{{ ldap_host }}"
    port: 636
    lookup_user: cn=admin,dc=example,dc=com
    lookup_password: password
    base_dn: dc=example,dc=com
    search_filter: "(memberof=cn=Users,dc=example,dc=com)"
    encryption: ssl
    crt_content: |
      -----BEGIN CERTIFICATE-----
      MIIDuz...
    type: ad
"""


from io import open
from functools import partial
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_module import TatlinModule


class TatlinLdapModule(TatlinModule):

    def __init__(self):
        argument_spec = {
            'host': {'type': 'str', 'required': False},
            'port': {'type': 'str', 'required': False},
            'lookup_user': {'type': 'str', 'required': False},
            'lookup_password': {
                'type': 'str',
                'required': False,
                'no_log': True,
            },
            'base_dn': {'type': 'str', 'required': False},
            'search_filter': {'type': 'str', 'required': False},
            'encryption': {
                'type': 'str',
                'choices': ['ssl', 'tls', 'off'],
                'required': False,
            },
            'crt_path': {'type': 'str', 'required': False},
            'crt_content': {'type': 'str', 'required': False},
            'user_attribute': {'type': 'str', 'required': False},
            'group_attribute': {'type': 'str', 'required': False},
            'type': {
                'type': 'str',
                'required': False,
                'choices': ['ad', 'custom']
            },
            'state': {
                'type': 'str',
                'required': False,
                'default': 'present',
                'choices': ['present', 'absent']
            },
        }

        mutually_exclusive = [('crt_path', 'crt_content')]
        required_if = [
            ('state', 'present', ('lookup_password',)),
            ('encryption', 'ssl', ('crt_path', 'crt_content'), True),
            ('encryption', 'tsl', ('crt_path', 'crt_content'), True),
        ]

        super(TatlinLdapModule, self).__init__(
            argument_spec=argument_spec,
            supports_check_mode=True,
            required_if=required_if,
            mutually_exclusive=mutually_exclusive,
        )

    def run(self):
        if self.params['type'] == 'ad' \
                and self.params['user_attribute'] is not None \
                and self.params['group_attribute'] is not None:
            self.fail_json(
                msg='Using "user_attribute" and "group_attribute" at '
                    'the same time with "type=ad" is prohibited',
                error='Mutually exclusive options',
                changed=False,
            )

        ldap_config = self.tatlin.get_ldap_config()
        action = None

        if self.params['state'] == 'present':
            changes = self.get_changes(ldap_config)
            if len(changes) > 0:
                if self.params['crt_path'] or self.params['crt_content']:
                    changes['cert'] = self.get_cert_content()

                action = partial(
                    ldap_config.update,
                    lookup_password=self.params['lookup_password'],
                    **changes)
        else:
            # Tatlin's API does not return ldap config state.
            # If ldap disabled, it returns empty strings as values.
            # So we assume that if host is empty, it means that ldap disabled.
            if ldap_config.host != '':
                action = ldap_config.reset

        if action is None:
            self.exit_json(msg='No changes required', changed=False)

        if not self.check_mode:
            action()

        self.exit_json(msg='Operation successful', changed=True)

    def get_changes(self, ldap_config):
        changes = {}

        for key in (
            'host',
            'port',
            'lookup_user',
            'base_dn',
            'search_filter',
            'encryption',
            'user_attribute',
            'group_attribute',
            'type',
        ):
            param = self.params[key]
            if param is not None and param != getattr(ldap_config, key):
                changes[key] = param

        return changes

    def get_cert_content(self):
        if self.params['crt_path']:
            with open(self.params['crt_path'], encoding='utf-8') as f:
                crt_content = f.read()
            return crt_content
        elif self.params['crt_content']:
            return self.params['crt_content']
        else:
            self.fail_json(
                msg='Please provide valid crt_path or crt_content options',
                error='Could not find certificate content',
                changed=False,
            )


def main():
    TatlinLdapModule()


if __name__ == "__main__":
    main()
