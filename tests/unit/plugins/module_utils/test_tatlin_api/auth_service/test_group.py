# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import json
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import check_object
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.auth.group import UserGroup
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import GROUPS_ENDPOINT
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import (
    OPEN_URL_FUNC, USER_GROUP_CLASS,
)


class TestGroup:

    def test_group_update(self, client, mock_method, open_url_kwargs):
        # Mock reload method
        mock_method(target=USER_GROUP_CLASS + '.reload')

        # Mock open_url method
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Create group
        group = UserGroup(
            client=client,
            name='testgroup',
            gid=3000,
        )

        # Update group comment
        group.update(comment='testcomment')

        # Defining expected call parameters
        open_url_kwargs.update(
            method='POST',
            url='https://localhost/{0}/{1}'.format(
                GROUPS_ENDPOINT, 'testgroup'),
            data=json.dumps({
                'displayName': 'testcomment',
                'memberOf': []
            }),
            headers={'Content-Type': 'application/json'},
        )

        # "Result: Request with expected parameters was sent to tatlin
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_group_update_no_args(self, client):
        # Create group
        group = UserGroup(
            client=client,
            name='testgroup',
            gid=3000,
        )

        # Check if TypeError raises when group updates without parameters
        with pytest.raises(TypeError):
            group.update()

    def test_users(self, client, mock_method):
        # Mock response with 2 users
        first_user = {
            'name': 'first_user',
            'enabled': True,
            'uid': 1100,
            'memberOf': ['testname'],
        }
        second_user = {
            'name': 'second_user',
            'enabled': False,
            'uid': 2000,
            'memberOf': ['testname', 'data']
        }

        mock_method(
            target=OPEN_URL_FUNC,
            first_user=first_user,
            second_user=second_user,
        )

        # Define expected data
        expected_users = [
            dict(name='first_user',
                 enabled=True,
                 uid=1100,),
            dict(name='second_user',
                 enabled=False,
                 uid=2000)]

        # Create group
        group = UserGroup(client=client, name='testname', gid=2000)

        # Result: 2 users with expected params was returned
        assert len(group.users) == 2
        for user in group.users:
            check_object(user, expected_users)

    def test_delete(self, client, mock_method, open_url_kwargs):
        # Mock open_url
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Create group
        group = UserGroup(
            client=client,
            name='testgroup',
            gid=3000,
        )

        # Delete group
        group.delete()

        # Defining expected call parameters
        open_url_kwargs.update(
            method='DELETE',
            url='https://localhost/{0}/{1}'.format(
                GROUPS_ENDPOINT, 'testgroup'),
        )

        # Result: Request with expected parameters was sent to tatlin
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_parent_groups(self, client, mock_method):
        # Mock reload method
        mock_method(target=USER_GROUP_CLASS + '.reload')

        # Mock response with 3 groups
        data = {
            'name': 'data',
            'gid': 1513,
            'displayName': 'Data users',
        }
        monitor = {
            'name': 'monitor',
            'gid': 1013,
            'displayName': 'Users with monitoring permissions',
        }
        testgroup = {
            'name': 'testgroup',
            'gid': 2001,
            'memberOf': [{'name': 'data'}, {'name': 'monitor'}],
        }

        mock_method(OPEN_URL_FUNC, data, monitor, testgroup)

        # Define expected data
        expected_groups = [
            dict(name='data',
                 gid=1513,
                 comment='Data users'),
            dict(name='monitor',
                 gid=1013,
                 comment='Users with monitoring permissions')]

        # Create child group
        group = UserGroup(
            client=client,
            name='testgroup',
            gid=2001,
            member_of=[{'name': 'data'}, {'name': 'monitor'}],
        )

        # Result: 2 parent groups with expected params was returned
        assert len(group.parent_groups) == 2
        for group in group.parent_groups:
            check_object(group, expected_groups)
