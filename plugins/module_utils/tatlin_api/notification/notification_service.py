# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.notification.snmp import SnmpConfig
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.notification.smtp import SmtpConfig

try:
    from typing import List, Dict
except ImportError:
    # Satisfy Python 2 which doesn't have typing.
    List = Dict = None


class NotificationService:

    def __init__(self, client):
        self._client = client

    def get_snmp_config(self):  # type: () -> SnmpConfig
        return SnmpConfig(client=self._client)

    def get_smtp_config(self):  # type: () -> SmtpConfig
        return SmtpConfig(client=self._client)
