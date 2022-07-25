# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json

from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.osmgr.ntp import NtpConfig
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import NTP_SERVERS_ENDPOINT
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import check_object
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import (
    OPEN_URL_FUNC, NTP_CONFIG_CLASS,
)


class TestNtp:

    def test_load(self, client, mock_method):
        # Save load method for future use
        init_load = NtpConfig.load

        # Mock method load without data
        mock_method(target=NTP_CONFIG_CLASS + '.load')

        # Create NtpConfig object
        ntp_config = NtpConfig(client)

        # Ensure that ntp_config has empty attributes
        check_object(ntp_config, {'servers': None})

        # Restore load method
        NtpConfig.load = init_load

        # Mock open_url with data
        mock_method(OPEN_URL_FUNC, ntp_server_list=['yadro.com'])

        # Load config
        ntp_config.load()

        # Result: ntp config with expected servers was returned
        check_object(ntp_config, {'servers': ['yadro.com']})

    def test_set_servers(self, client, mock_method, open_url_kwargs):
        # Mock open_url with servers data
        mock_method(
            target=OPEN_URL_FUNC,
            ntp_server_list=['1.1.1.1'],
        )

        # Create NtpConfig object
        ntp_config = NtpConfig(client)

        # Mock load method without data
        mock_method(NTP_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Set servers
        ntp_config.set_servers(['yadro.com', '2.2.2.2'])

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(NTP_SERVERS_ENDPOINT),
            data=json.dumps({'ntp_server_list': ['yadro.com', '2.2.2.2']}),
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_add_server(self, client, mock_method, open_url_kwargs):
        # Mock open_url with servers data
        mock_method(target=OPEN_URL_FUNC, ntp_server_list=['yadro.com'])

        # Create NtpConfig object
        ntp_config = NtpConfig(client)

        # Mock load method without data
        mock_method(NTP_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Add server
        ntp_config.add_server('1.1.1.1')

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(NTP_SERVERS_ENDPOINT),
            data=json.dumps({'ntp_server_list': ['yadro.com', '1.1.1.1']}),
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_remove_server(self, client, mock_method, open_url_kwargs):
        # Mock open_url with servers data
        mock_method(
            target=OPEN_URL_FUNC,
            ntp_server_list=['yadro.com', '1.1.1.1', '2.2.2.2'],
        )

        # Create NtpConfig object
        ntp_config = NtpConfig(client)

        # Mock load method without data
        mock_method(NTP_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Remove server
        ntp_config.remove_server('1.1.1.1')

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(NTP_SERVERS_ENDPOINT),
            data=json.dumps({'ntp_server_list': ['yadro.com', '2.2.2.2']}),
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_reset_servers(self, client, mock_method, open_url_kwargs):
        # Mock open_url with servers data
        mock_method(
            target=OPEN_URL_FUNC,
            ntp_server_list=['yadro.com', '1.1.1.1', '2.2.2.2'],
        )

        # Create NtpConfig object
        ntp_config = NtpConfig(client)

        # Mock load method without data
        mock_method(NTP_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Reset servers
        ntp_config.reset_servers()

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(NTP_SERVERS_ENDPOINT),
            data=json.dumps({'ntp_server_list': []}),
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        open_url_mock.assert_called_with(**open_url_kwargs)
