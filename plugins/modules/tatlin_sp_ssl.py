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
module: tatlin_sp_ssl
short_description: Set storage SSL certificate
version_added: "1.0.0"
description:
  - This module is intended to set SSL certificate
  - This module supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin_uni.connection_options
options:
  crt_path:
    type: str
    required: False
    description: Path to file with SSL certificate
  key_path:
    type: str
    required: False
    description: Path to file with private key
  crt_content:
    type: str
    required: False
    description: Content of SSL certificate
  key_content:
    type: str
    required: False
    description: Content of private key
notes:
  - One of following options are required - crt_path or crt_content,
    key_path or key_content
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
- name: Upload certificate from path
  yadro.tatlin_uni.tatlin_sp_ssl:
    connection: "{{ connection }}"
    crt_path: /etc/ssl/certs/testssl.pem
    key_path: /etc/ssl/private/testssl.key

- name: Test upload SSL certificate | Upload certificate from content
  yadro.tatlin_uni.tatlin_sp_ssl:
    connection: "{{ connection }}"
    crt_content: |
      -----BEGIN CERTIFICATE-----
      MIIFuzCCA6OgAwIBAgIU...
      -----END CERTIFICATE-----
    key_content: |
      -----BEGIN PRIVATE KEY-----
      MIIJQwIBADANBgkqhkiG9w...
      -----END PRIVATE KEY-----
"""


from io import open
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_module import TatlinModule


class TatlinSslModule(TatlinModule):

    def __init__(self):
        argument_spec = {
            'crt_path': {'type': 'str', 'required': False},
            'key_path': {'type': 'str', 'required': False, 'no_log': True},
            'crt_content': {'type': 'str', 'required': False},
            'key_content': {'type': 'str', 'required': False, 'no_log': True},
        }

        required_one_of = [
            ('crt_path', 'crt_content'),
            ('key_path', 'key_content'),
        ]
        mutually_exclusive = [
            ('crt_path', 'crt_content'),
            ('key_path', 'key_content'),
        ]

        super(TatlinSslModule, self).__init__(
            argument_spec=argument_spec,
            supports_check_mode=True,
            required_one_of=required_one_of,
            mutually_exclusive=mutually_exclusive,
        )

    def run(self):
        crt = self.get_cert_content()
        key = self.get_key_content()

        if not self.check_mode:
            self.tatlin.upload_ssl_certificate(crt, key)

        self.exit_json(msg='Operation successful', changed=True)

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

    def get_key_content(self):
        if self.params['key_path']:
            with open(self.params['key_path'], encoding='utf-8') as f:
                crt_content = f.read()
            return crt_content
        elif self.params['key_content']:
            return self.params['key_content']


def main():
    TatlinSslModule()


if __name__ == "__main__":
    main()
