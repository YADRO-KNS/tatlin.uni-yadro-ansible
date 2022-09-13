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
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.models.host_group import HostGroup
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import (
    OPEN_URL_FUNC, TATLIN_API_CLIENT_CLASS, HOST_GROUP_CLASS
)
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import (
    check_called_with,
)


class TestHostGroup:

    def test_create_host_group(
        self, tatlin, make_mock, hosts_data, open_url_kwargs
    ):
        # Mock open_url without data
        open_url_mock = make_mock(OPEN_URL_FUNC)

        # Create hosts objects
        host1 = Host(client=tatlin, **hosts_data[0])
        host2 = Host(client=tatlin, **hosts_data[1])

        # Create host group
        tatlin.create_host_group(
            name='testgroup',
            tags=['123', '321'],
            hosts=[host1, host2]
        )

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(
                eps.PERSONALITIES_HOST_GROUPS_ENDPOINT),
            data={
                'name': 'testgroup',
                'tags': ['123', '321'],
                'host_ids': [
                    '7ab276b8-59a3-416b-8f28-191e91b4e20b',
                    '9355f65d-a8a2-4df9-8459-98a5c20725f3',
                ]
            },
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        check_called_with(open_url_mock, **open_url_kwargs)

    def test_get_host_groups(
        self, tatlin, make_mock, host_groups_data, hosts_data
    ):
        # Mock open_url response with data
        make_mock(OPEN_URL_FUNC, return_value=host_groups_data)

        # Create hosts objects
        host1 = Host(client=tatlin, **hosts_data[0])
        host2 = Host(client=tatlin, **hosts_data[1])

        # Mock get_hosts with created hosts
        make_mock(
            target=TATLIN_API_CLIENT_CLASS + '.get_hosts',
            return_value=[host1, host2],
        )

        # Get host groups
        host_groups = tatlin.get_host_groups()

        # Result: Host groups with expected parameters were returned
        assert host_groups[0].name == 'hostgroup1'
        assert host_groups[0].id == '02a41332-626f-40a7-a755-94650640477b'
        assert host_groups[0].tags == ['tag1', 'tag2']
        assert host_groups[0].hosts == [host1, host2]

        assert host_groups[1].name == 'hostgroup2'
        assert host_groups[1].id == 'a43aaf85-ad1d-4ac7-9433-09992c36a29a'
        assert host_groups[1].tags == []
        assert host_groups[1].hosts == []

    def test_get_host_group(
        self, tatlin, make_mock, host_groups_data, hosts_data
    ):
        # Mock open_url response with data
        make_mock(OPEN_URL_FUNC, return_value=host_groups_data)

        # Create hosts objects
        host1 = Host(client=tatlin, **hosts_data[0])
        host2 = Host(client=tatlin, **hosts_data[1])

        # Mock get_hosts with created hosts
        make_mock(
            target=TATLIN_API_CLIENT_CLASS + '.get_hosts',
            return_value=[host1, host2],
        )

        # Get host group
        host_group = tatlin.get_host_group('hostgroup1')

        # Result: Host group with expected parameters were returned
        assert host_group.name == 'hostgroup1'
        assert host_group.id == '02a41332-626f-40a7-a755-94650640477b'
        assert host_group.tags == ['tag1', 'tag2']
        assert host_group.hosts == [host1, host2]

    def test_host_group_load(
        self, tatlin, make_mock, host_groups_data, hosts_data
    ):
        # Create empty HostGroup object
        host_group = HostGroup(client=tatlin)

        # Mock open_url response with data
        make_mock(OPEN_URL_FUNC, return_value=host_groups_data[0])

        # Create hosts objects
        host1 = Host(client=tatlin, **hosts_data[0])
        host2 = Host(client=tatlin, **hosts_data[1])

        # Mock get_hosts with created hosts
        make_mock(
            target=TATLIN_API_CLIENT_CLASS + '.get_hosts',
            return_value=[host1, host2],
        )

        # Load host group
        host_group.load()

        # Result: Host group has expected parameters
        assert host_group.name == 'hostgroup1'
        assert host_group.id == '02a41332-626f-40a7-a755-94650640477b'
        assert host_group.tags == ['tag1', 'tag2']
        assert host_group.hosts == [host1, host2]

    def test_host_group_set_hosts(
        self, tatlin, make_mock, open_url_kwargs, host_groups_data, hosts_data
    ):
        # Create HostGroup object
        host_group = HostGroup(client=tatlin, **host_groups_data[0])

        # Mock open_url response without data
        open_url_mock = make_mock(OPEN_URL_FUNC)

        # Mock load method
        load_mock = make_mock(HOST_GROUP_CLASS + '.load')

        # Create host object
        host = Host(client=tatlin, **hosts_data[0])

        # Set new host
        host_group.set_hosts(host)

        # Define expected call parameters
        open_url_kwargs.update(
            method='POST',
            url='https://localhost/{0}'.format(
                eps.PERSONALITIES_HOST_GROUPS_ENDPOINT),
            headers={'Content-Type': 'application/json'},
            data={
                'id': host_group.id,
                'name': host_group.name,
                'host_ids': [host.id],
                'tags': host_group.tags,
            },
        )

        check_called_with(open_url_mock, **open_url_kwargs)
        load_mock.assert_called_once()

    @pytest.mark.parametrize(
        'new_tags, expected_tags', [
            (['tag3', 'tag4'], ['tag3', 'tag4']),
            ('tag5', ['tag5'])
        ]
    )
    def test_host_group_set_tags(
        self,
        tatlin,
        make_mock,
        host_groups_data,
        open_url_kwargs,
        new_tags,
        expected_tags,
    ):

        # Create HostGroup object
        host_group = HostGroup(client=tatlin, **host_groups_data[0])

        # Mock open_url response without data
        open_url_mock = make_mock(OPEN_URL_FUNC)

        # Mock load method
        load_mock = make_mock(HOST_GROUP_CLASS + '.load')

        # Set new tags
        host_group.set_tags(tags=new_tags)

        # Define expected call parameters
        open_url_kwargs.update(
            method='POST',
            url='https://localhost/{0}'.format(
                eps.PERSONALITIES_HOST_GROUPS_ENDPOINT),
            headers={'Content-Type': 'application/json'},
            data={
                'id': host_group.id,
                'name': host_group.name,
                'host_ids': host_groups_data[0]['host_ids'],
                'tags': expected_tags,
            },
        )

        check_called_with(open_url_mock, **open_url_kwargs)
        load_mock.assert_called_once()
