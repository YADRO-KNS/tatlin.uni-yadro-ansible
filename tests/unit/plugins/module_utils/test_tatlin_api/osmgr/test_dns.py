# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import pytest
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.models.dns import DnsConfig
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import DNS_CONFIG_ENDPOINT
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import check_obj
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import (
    DNS_CONFIG_CLASS, OPEN_URL_FUNC)


class TestDns:

    def test_get_dns_filled_config(self, tatlin, make_mock):
        # Mock open_url response with data
        make_mock(
            OPEN_URL_FUNC,
            return_value={
                'dns_static_servers': ['127.0.0.1', '1.1.1.1'],
                'dns_static_search_list': ['exapmle.com', 'test.com']
            }
        )

        # Get DNS config
        dns_config = tatlin.get_dns_config()

        # Result: DNS config with expected parameters was returned
        assert dns_config.servers == ['127.0.0.1', '1.1.1.1']
        assert dns_config.search_list == ['exapmle.com', 'test.com']

    def test_get_dns_empty_config(self, tatlin, make_mock):
        # Mock open_url response with data
        make_mock(
            OPEN_URL_FUNC,
            return_value={
                'dns_static_servers': [],
                'dns_static_search_list': [],
            }
        )

        # Get DNS config
        dns_config = tatlin.get_dns_config()

        # Result: DNS config with expected parameters was returned
        assert dns_config.servers == []
        assert dns_config.search_list == []

    def test_load(self, tatlin, make_mock):
        # Save load method for future use
        init_load = DnsConfig.load

        # Mock method load without data
        make_mock(target=DNS_CONFIG_CLASS + '.load')

        # Create DnsConfig object
        dns_config = DnsConfig(tatlin)

        # Ensure that dns_config has empty attributes
        check_obj(dns_config, {'servers': [], 'search_list': []})

        # Restore load method
        DnsConfig.load = init_load

        # Mock open_url with data
        make_mock(
            OPEN_URL_FUNC,
            return_value={
                'dns_static_servers': ['127.0.0.1'],
                'dns_static_search_list': ['exapmle.com'],
            }
        )

        # Load config
        dns_config.load()

        # Result: dns config with expected servers was returned
        check_obj(
            dns_config,
            {'servers': ['127.0.0.1'], 'search_list': ['exapmle.com']}
        )

    @pytest.mark.parametrize(
        'new_servers', [['2.2.2.2', '3.3.3.3'], '2.2.2.2']
    )
    def test_update_servers(
        self, tatlin, make_mock, open_url_kwargs, new_servers,
    ):
        # Mock open_url with servers data
        make_mock(
            target=OPEN_URL_FUNC,
            return_value={
                'dns_static_servers': ['1.1.1.1'],
                'dns_static_search_list': [],
            }
        )

        # Create DnsConfig object
        dns_config = DnsConfig(tatlin)

        # Mock load method without data
        make_mock(DNS_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Set servers
        dns_config.update(servers=new_servers)

        # Defining expected call parameters
        def to_list(x):
            return [x] if isinstance(x, str) else x

        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(DNS_CONFIG_ENDPOINT),
            data=json.dumps({
                'dns_static_servers': to_list(new_servers),
                'dns_static_search_list': [],
            }),
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        open_url_mock.assert_called_with(**open_url_kwargs)

    @pytest.mark.parametrize(
        'new_suffixes', [['example.com', 'test.com'], 'example.com']
    )
    def test_update_search_list(
        self, tatlin, make_mock, open_url_kwargs, new_suffixes
    ):
        # Mock open_url with servers data
        make_mock(
            target=OPEN_URL_FUNC,
            return_value={
                'dns_static_servers': ['1.1.1.1'],
                'dns_static_search_list': [],
            }
        )

        # Create DnsConfig object
        dns_config = DnsConfig(tatlin)

        # Mock load method without data
        make_mock(DNS_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Set search_list
        dns_config.update(search_list=new_suffixes)

        # Defining expected call parameters
        def to_list(x):
            return [x] if isinstance(x, str) else x

        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(DNS_CONFIG_ENDPOINT),
            data=json.dumps({
                'dns_static_servers': ['1.1.1.1'],
                'dns_static_search_list': to_list(new_suffixes),
            }),
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_reset(self, tatlin, make_mock, open_url_kwargs):
        # Mock open_url with servers data
        make_mock(
            target=OPEN_URL_FUNC,
            return_value={
                'dns_static_servers': ['1.1.1.1', '2.2.2.2'],
                'dns_static_search_list': ['example.com', 'test.com'],
            }
        )

        # Create DnsConfig object
        dns_config = DnsConfig(tatlin)

        # Mock load method without data
        make_mock(DNS_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Reset DNS config
        dns_config.reset()

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(DNS_CONFIG_ENDPOINT),
            data=json.dumps({
                'dns_static_servers': [],
                'dns_static_search_list': [],
            }),
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_add_server(self, tatlin, make_mock, open_url_kwargs):
        # Mock open_url with servers data
        make_mock(
            target=OPEN_URL_FUNC,
            return_value={
                'dns_static_servers': ['1.1.1.1'],
                'dns_static_search_list': ['example.com'],
            }
        )

        # Create DnsConfig object
        dns_config = DnsConfig(tatlin)

        # Mock load method without data
        make_mock(DNS_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Add server
        dns_config.add_server('2.2.2.2')

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(DNS_CONFIG_ENDPOINT),
            data=json.dumps({
                'dns_static_servers': ['1.1.1.1', '2.2.2.2'],
                'dns_static_search_list': ['example.com'],
            }),
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_add_suffix(self, tatlin, make_mock, open_url_kwargs):
        # Mock open_url with servers data
        make_mock(
            target=OPEN_URL_FUNC,
            return_value={
                'dns_static_servers': ['1.1.1.1'],
                'dns_static_search_list': ['example.com'],
            }
        )

        # Create DnsConfig object
        dns_config = DnsConfig(tatlin)

        # Mock load method without data
        make_mock(DNS_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Add suffix
        dns_config.add_suffix('test.com')

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(DNS_CONFIG_ENDPOINT),
            data=json.dumps({
                'dns_static_servers': ['1.1.1.1'],
                'dns_static_search_list': ['example.com', 'test.com'],
            }),
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_remove_server(self, tatlin, make_mock, open_url_kwargs):
        # Mock open_url with servers data
        make_mock(
            target=OPEN_URL_FUNC,
            return_value={
                'dns_static_servers': ['1.1.1.1', '2.2.2.2', '3.3.3.3'],
                'dns_static_search_list': ['example.com'],
            }
        )

        # Create DnsConfig object
        dns_config = DnsConfig(tatlin)

        # Mock load method without data
        make_mock(DNS_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Remove server
        dns_config.remove_server('2.2.2.2')

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(DNS_CONFIG_ENDPOINT),
            data=json.dumps({
                'dns_static_servers': ['1.1.1.1', '3.3.3.3'],
                'dns_static_search_list': ['example.com'],
            }),
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_remove_suffix(self, tatlin, make_mock, open_url_kwargs):
        # Mock open_url with servers data
        make_mock(
            target=OPEN_URL_FUNC,
            return_value={
                'dns_static_servers': ['1.1.1.1'],
                'dns_static_search_list': ['example.com', 'test.com', 'yadro.com'],
            }
        )

        # Create DnsConfig object
        dns_config = DnsConfig(tatlin)

        # Mock load method without data
        make_mock(DNS_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Remove suffix
        dns_config.remove_suffix('test.com')

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(DNS_CONFIG_ENDPOINT),
            data=json.dumps({
                'dns_static_servers': ['1.1.1.1'],
                'dns_static_search_list': ['example.com', 'yadro.com'],
            }),
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        open_url_mock.assert_called_with(**open_url_kwargs)
