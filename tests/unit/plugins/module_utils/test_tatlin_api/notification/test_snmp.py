# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import json
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.models.snmp import SnmpConfig
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import SNMP_ENDPOINT
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import check_obj
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import (
    OPEN_URL_FUNC, SNMP_CONFIG_CLASS,
)


class TestSnmp:

    def test_get_snmp_config(self, tatlin, mock_method):
        # Mock open_url response with data
        mock_method(
            OPEN_URL_FUNC,
            community='tatlin',
            recipients={'127.0.0.1:162': {}}
        )

        # Call get_snmp_config
        snmp_config = tatlin.get_snmp_config()

        # Result: Config with expected server was returned
        assert snmp_config.community == 'tatlin'
        assert snmp_config.servers == ['127.0.0.1:162']

    def test_load(self, tatlin, mock_method):
        # Save load method for future use
        init_load = SnmpConfig.load

        # Mock method load without data
        mock_method(target=SNMP_CONFIG_CLASS + '.load')

        # Create SnmpConfig object
        snmp_config = SnmpConfig(tatlin)

        # Ensure that port has empty attributes
        check_obj(snmp_config, {'community': None, 'servers': []})

        # Restore load method
        SnmpConfig.load = init_load

        # Mock open_url with data
        mock_method(
            OPEN_URL_FUNC,
            community='tatlin',
            recipients={'127.0.0.1:162': {}}
        )

        # Load config
        snmp_config.load()

        # Result: SNMP config with expected servers was returned
        check_obj(
            snmp_config,
            {'community': 'tatlin', 'servers': ['127.0.0.1:162']}
        )

    def test_update_community(self, tatlin, mock_method, open_url_kwargs):
        # Mock open_url with servers data
        mock_method(
            target=OPEN_URL_FUNC,
            community='tatlin',
        )

        # Create SnmpConfig object
        snmp_config = SnmpConfig(tatlin)

        # Mock load method without data
        mock_method(SNMP_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Set community
        snmp_config.update(community='tatlin')

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(SNMP_ENDPOINT),
            data=json.dumps({'community': 'tatlin', 'recipients': {}}),
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_update_servers(self, tatlin, mock_method, open_url_kwargs):
        # Mock open_url with servers data
        mock_method(
            target=OPEN_URL_FUNC,
            community='tatlin',
            recipients={'1.1.1.1:1': {}}
        )

        # Create SnmpConfig object
        snmp_config = SnmpConfig(tatlin)

        # Mock load method without data
        mock_method(SNMP_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Set servers
        snmp_config.update(servers=['127.0.0.1:162', 'example.com:1'])

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(SNMP_ENDPOINT),
            data=json.dumps({
                'community': 'tatlin',
                'recipients': {'127.0.0.1:162': {},
                               'example.com:1': {}}
            }),
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_update_all_attributes(self, tatlin, mock_method, open_url_kwargs):
        # Mock open_url with servers data
        mock_method(
            target=OPEN_URL_FUNC,
            community='tatlin',
            recipients={'1.1.1.1:1': {}}
        )

        # Create SnmpConfig object
        snmp_config = SnmpConfig(tatlin)

        # Mock load method without data
        mock_method(SNMP_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Set community and servers
        snmp_config.update(
            community='test_community',
            servers=['127.0.0.1:162', 'example.com:1']
        )

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(SNMP_ENDPOINT),
            data=json.dumps({
                'community': 'test_community',
                'recipients': {'127.0.0.1:162': {},
                               'example.com:1': {}}
            }),
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_reset(self, tatlin, mock_method, open_url_kwargs):
        # Mock open_url with servers data
        mock_method(
            target=OPEN_URL_FUNC,
            community='tatlin',
            recipients={'1.1.1.1:1': {}}
        )

        # Create SnmpConfig object
        snmp_config = SnmpConfig(tatlin)

        # Mock load method without data
        mock_method(SNMP_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Reset config
        snmp_config.reset()

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(SNMP_ENDPOINT),
            data=None,
        )

        # Result: open_url was called with expected params
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_add_server(self, tatlin, mock_method, open_url_kwargs):
        # Mock open_url with servers data
        mock_method(
            target=OPEN_URL_FUNC,
            community='tatlin',
            recipients={'127.0.0.1:162': {}, 'example.com:1': {}}
        )

        # Create SnmpConfig object
        snmp_config = SnmpConfig(tatlin)

        # Mock load method without data
        mock_method(SNMP_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Add server
        snmp_config.add_server('test.com:162')

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(SNMP_ENDPOINT),
            data=json.dumps({
                'community': 'tatlin',
                'recipients': {'127.0.0.1:162': {},
                               'example.com:1': {},
                               'test.com:162': {}},
            }),
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_remove_server_with_port(self, tatlin, mock_method, open_url_kwargs):
        # Mock open_url with servers data
        mock_method(
            target=OPEN_URL_FUNC,
            community='tatlin',
            recipients={
                '127.0.0.1:162': {}, 'example.com:1': {}, 'example.com:2': {},
            }
        )

        # Create SnmpConfig object
        snmp_config = SnmpConfig(tatlin)

        # Mock load method without data
        mock_method(SNMP_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Remove server
        snmp_config.remove_server('example.com:1')

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(SNMP_ENDPOINT),
            data=json.dumps({
                'community': 'tatlin',
                'recipients': {'127.0.0.1:162': {}, 'example.com:2': {}},
            }),
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_remove_server_without_port(self, tatlin, mock_method, open_url_kwargs):
        # Mock open_url with servers data
        mock_method(
            target=OPEN_URL_FUNC,
            community='tatlin',
            recipients={
                '127.0.0.1:162': {}, 'example.com:1': {}, 'example.com:2': {},
            }
        )

        # Create SnmpConfig object
        snmp_config = SnmpConfig(tatlin)

        # Mock load method without data
        mock_method(SNMP_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Remove server
        snmp_config.remove_server('example.com')

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(SNMP_ENDPOINT),
            data=json.dumps({
                'community': 'tatlin',
                'recipients': {'127.0.0.1:162': {}},
            }),
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        open_url_mock.assert_called_with(**open_url_kwargs)

    @pytest.mark.parametrize('new_server', ['1.1.1.1', 'test.com'])
    def test_update_servers_with_wrong_addresses(
        self, tatlin, mock_method, open_url_kwargs, new_server,
    ):
        # Mock open_url with servers data
        mock_method(
            target=OPEN_URL_FUNC,
            community='tatlin',
            recipients={'1.1.1.1:1': {}}
        )

        # Create SnmpConfig object
        snmp_config = SnmpConfig(tatlin)

        # Mock load method without data
        mock_method(SNMP_CONFIG_CLASS + '.load')

        # Set servers with exception
        with pytest.raises(TatlinClientError) as exc_info:
            snmp_config.update(servers=['127.0.0.1:162', new_server])

        # Result: Exception with corresponding text was raised
        assert str(exc_info.value) == 'Wrong server address format. ' \
                                      'Must be IP:port or FQDN:port'
