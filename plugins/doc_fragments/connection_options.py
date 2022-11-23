# -*- coding: utf-8 -*-

# YADRO Tatlin Unified Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    DOCUMENTATION = r"""
    options:
      connection:
        required: True
        type: dict
        description:
          - I(connection) describes Tatlin Storage Processor (SP) connection configuration.
          - Only session connection supported.
          - Authorization is executed automatically with corresponding endpoint. 'auth/login' by default.
          - Client receives x-auth-token and uses it for following requests.
        suboptions:
          base_url:
            required: True
            type: str
            description: Tatlin REST API entrypoint.
          username:
            type: str
            description: Tatlin username to login.
          password:
            type: str
            description: Tatlin user password.
          validate_certs:
            type: bool
            default: True
            description:
              - Responsible for SSL certificates validation.
              - If set to False certificates won't validated.
          timeout:
            type: int
            default: 60
            description: Tatlin REST API request timeout.
"""
