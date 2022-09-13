# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints as eps
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.models.host import Host
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import (
    TatlinClientError,
)
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import (
    HOST_CLASS,
)
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import (
    check_called_with,
)
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import (
    OPEN_URL_FUNC,
)


class TestHost:

    def test_create_host_mutual_auth(
        self, tatlin, make_mock, open_url_kwargs
    ):
        # Mock open_url without data
        open_url_mock = make_mock(OPEN_URL_FUNC)

        # Create host
        tatlin.create_host(
            name='host1',
            port_type='eth',
            ports='iqn',
            tags=['tag1', 'tag2'],
            auth='mutual',
            username='username',
            password='password',
            mutual_username='mutualname',
            mutual_password='mutualpass',
        )

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(
                eps.PERSONALITIES_HOSTS_ENDPOINT),
            data={
                'name': 'host1',
                'port_type': 'iscsi',
                'initiators': ['iqn'],
                'tags': ['tag1', 'tag2'],
                'auth': {
                    'auth_type': 'mutual',
                    'internal_name': 'username',
                    'internal_password': 'password',
                    'external_name': 'mutualname',
                    'external_password': 'mutualpass',
                }
            },
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        check_called_with(open_url_mock, **open_url_kwargs)

    @pytest.mark.parametrize(
        'username, password, mutual_username, mutual_password', (
            [None, 'pass', 'mutualname', 'mutualpass'],
            ['name', None, 'mutualname', 'mutualpass'],
            ['name', 'pass', None, 'mutualpass'],
            ['name', 'pass', 'mutualname', None],
        )
    )
    def test_create_host_mutual_auth_fail(
        self,
        tatlin,
        make_mock,
        open_url_kwargs,
        username,
        password,
        mutual_username,
        mutual_password,
    ):
        # Mock open_url without data
        make_mock(OPEN_URL_FUNC)

        # Create host without one of login params
        # Result: Error was raised
        with pytest.raises(TatlinClientError):
            tatlin.create_host(
                name='host1',
                port_type='eth',
                ports='iqn',
                tags=['tag1', 'tag2'],
                auth='mutual',
                username=username,
                password=password,
                mutual_username=mutual_username,
                mutual_password=mutual_password,
            )

    def test_create_host_oneway_auth(
        self, tatlin, make_mock, open_url_kwargs,
    ):
        # Mock open_url without data
        open_url_mock = make_mock(OPEN_URL_FUNC)

        # Create host
        tatlin.create_host(
            name='host1',
            port_type='eth',
            ports='iqn',
            tags=['tag1', 'tag2'],
            auth='oneway',
            username='username',
            password='password',
        )

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(
                eps.PERSONALITIES_HOSTS_ENDPOINT),
            data={
                'name': 'host1',
                'port_type': 'iscsi',
                'initiators': ['iqn'],
                'tags': ['tag1', 'tag2'],
                'auth': {
                    'auth_type': 'oneway',
                    'internal_name': 'username',
                    'internal_password': 'password',
                }
            },
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        check_called_with(open_url_mock, **open_url_kwargs)

    @pytest.mark.parametrize(
        'username, password', (
            ['user', None],
            [None, 'pass'],
        )
    )
    def test_create_host_oneway_auth_fail(
        self, tatlin, make_mock, open_url_kwargs, username, password,
    ):
        # Mock open_url without data
        make_mock(OPEN_URL_FUNC)

        # Create host without one of login params
        # Result: Error was raised
        with pytest.raises(TatlinClientError):
            tatlin.create_host(
                name='host1',
                port_type='eth',
                ports='iqn',
                tags=['tag1', 'tag2'],
                auth='oneway',
                username=username,
                password=password,
            )

    def test_create_host_none_auth(
        self, tatlin, make_mock, open_url_kwargs,
    ):
        # Mock open_url without data
        open_url_mock = make_mock(OPEN_URL_FUNC)

        # Create host
        tatlin.create_host(
            name='host1',
            port_type='eth',
            ports='iqn',
            tags=['tag1', 'tag2'],
            auth='none',
        )

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(
                eps.PERSONALITIES_HOSTS_ENDPOINT),
            data={
                'name': 'host1',
                'port_type': 'iscsi',
                'initiators': ['iqn'],
                'tags': ['tag1', 'tag2'],
                'auth': {'auth_type': 'none'},
            },
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        check_called_with(open_url_mock, **open_url_kwargs)

    def test_get_hosts(self, tatlin, make_mock, open_url_kwargs, hosts_data):
        # Mock open_url response with data
        make_mock(OPEN_URL_FUNC, return_value=hosts_data)

        # Get hosts
        hosts = tatlin.get_hosts()

        # Result: hosts with expected parameters were returned
        assert hosts[0].auth == 'mutual'
        assert hosts[0].id == '7ab276b8-59a3-416b-8f28-191e91b4e20b'
        assert hosts[0].mutual_username == 'targetname'
        assert hosts[0].name == 'host1'
        assert hosts[0].port_type == 'eth'
        assert hosts[0].ports == ['iqn.1993-08.org.debian:01:5728e30474c']
        assert hosts[0].tags == ['tag1', 'tag2']
        assert hosts[0].username == 'hostname'

        assert hosts[1].auth == 'none'
        assert hosts[1].id == '9355f65d-a8a2-4df9-8459-98a5c20725f3'
        assert hosts[1].mutual_username is None
        assert hosts[1].name == 'host2'
        assert hosts[1].port_type == 'eth'
        assert hosts[1].ports == []
        assert hosts[1].tags == ['testtag']
        assert hosts[1].username is None

    def test_get_host(self, tatlin, make_mock, open_url_kwargs, hosts_data):
        # Mock open_url response with data
        make_mock(OPEN_URL_FUNC, return_value=hosts_data)

        # Get host by name
        host = tatlin.get_host('host1')

        # Result: host with expected parameters was returned
        assert host.auth == 'mutual'
        assert host.id == '7ab276b8-59a3-416b-8f28-191e91b4e20b'
        assert host.mutual_username == 'targetname'
        assert host.name == 'host1'
        assert host.port_type == 'eth'
        assert host.ports == ['iqn.1993-08.org.debian:01:5728e30474c']
        assert host.tags == ['tag1', 'tag2']
        assert host.username == 'hostname'

    def test_host_load(self, tatlin, make_mock, hosts_data):
        # Create empty Host object
        host = Host(client=tatlin, id='host_id')

        # Mock open_url response with data
        make_mock(OPEN_URL_FUNC, return_value=hosts_data[0])

        # Load host
        host.load()

        # Result: host object has expected parameters
        assert host.auth == 'mutual'
        assert host.id == '7ab276b8-59a3-416b-8f28-191e91b4e20b'
        assert host.mutual_username == 'targetname'
        assert host.name == 'host1'
        assert host.port_type == 'eth'
        assert host.ports == ['iqn.1993-08.org.debian:01:5728e30474c']
        assert host.tags == ['tag1', 'tag2']
        assert host.username == 'hostname'

    def test_host_update(
        self, tatlin, make_mock, open_url_kwargs, hosts_data,
    ):
        # Create empty Host object
        host = Host(client=tatlin, id='host_id')

        # Mock open_url response with data
        make_mock(OPEN_URL_FUNC, return_value=hosts_data[0])

        # Load host
        host.load()

        # Mock open_url response without data
        open_url_mock = make_mock(OPEN_URL_FUNC)

        # Mock load method
        load_mock = make_mock(HOST_CLASS + '.load')

        # Update host params
        host.update(
            ports='new_port',
            tags=['new_tag1', 'new_tag2'],
            auth='oneway',
            username='newname',
            password='newpass',
        )

        # Defining expected call parameters
        open_url_kwargs.update(
            method='POST',
            url='https://localhost/{0}'.format(
                eps.PERSONALITIES_HOSTS_ENDPOINT),
            headers={'Content-Type': 'application/json'},
            data={
                'id': host.id,
                'name': host.name,
                'port_type': 'iscsi',
                'initiators': ['new_port'],
                'tags': ['new_tag1', 'new_tag2'],
                'auth': {
                    'auth_type': 'oneway',
                    'internal_name': 'newname',
                    'internal_password': 'newpass',
                }
            },
        )

        check_called_with(open_url_mock, **open_url_kwargs)
        load_mock.assert_called_once()
