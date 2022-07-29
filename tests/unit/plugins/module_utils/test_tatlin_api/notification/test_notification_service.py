# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import OPEN_URL_FUNC
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import check_object


class TestNotificationService:

    def test_get_snmp_config(self, client, mock_method):
        # Mock open_url response with data
        mock_method(
            OPEN_URL_FUNC,
            community='tatlin',
            recipients={'127.0.0.1:162': {}}
        )

        # Call get_snmp_config
        snmp_config = client.notification_service.get_snmp_config()

        # Result: Config with expected server was returned
        assert snmp_config.community == 'tatlin'
        assert snmp_config.servers == ['127.0.0.1:162']

    def test_get_smtp_config(self, client, mock_method):
        # Mock open_url response with data
        mock_method(
            OPEN_URL_FUNC,
            host='127.0.0.1',
            port=25,
            protocol='',
            login={'username': 'admin', 'password': '***REMOVED***'},
            sender_email='smtp@example.com',
            recipients={
                'first@recipients.com': {},
                'second@recipients.com': {},
            }
        )

        # Call get_smtp_config
        smtp_config = client.notification_service.get_smtp_config()

        # Define expected params
        exp_params = {
            'address': '127.0.0.1',
            'port': 25,
            'encryption': 'off',
            'login': 'admin',
            'sender': 'smtp@example.com',
            'recipients': ['first@recipients.com', 'second@recipients.com'],
        }

        # Result: Config with expected server was returned
        check_object(smtp_config, exp_params)
