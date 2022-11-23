# -*- coding: utf-8 -*-

# YADRO Tatlin Unified Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import json
from ansible_collections.yadro.tatlin_uni.tests.unit.plugins.module_utils.test_tatlin_api.utils import check_obj
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.models.user_group import UserGroup
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.endpoints import GROUPS_ENDPOINT
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.exception import (
    TatlinClientError, RESTClientNotFoundError,
)
from ansible_collections.yadro.tatlin_uni.tests.unit.plugins.module_utils.test_tatlin_api.constants import (
    OPEN_URL_FUNC, USER_GROUP_CLASS, TATLIN_API_CLIENT_CLASS, REST_CLIENT_CLASS,
)


class TestUserGroup:

    def test_get_user_groups(self, tatlin, make_mock):
        # Mock get_groups method with 2 groups
        admin = {
            'name': 'admin',
            'gid': 1100,
            'displayName': 'Administrative group',
        }
        testgroup = {
            'name': 'testgroup',
            'gid': 2001,
            'memberOf': [{'name': 'admin'}],
        }

        make_mock(OPEN_URL_FUNC, return_value=[admin, testgroup])

        # Define expected data
        expected_groups = [
            dict(name='admin',
                 gid=1100,
                 comment='Administrative group'),
            dict(name='testgroup',
                 gid=2001,
                 comment='')]

        # Get all tatlin groups
        groups = tatlin.get_user_groups()

        # Result: 2 groups with expected params was returned
        assert len(groups) == 2
        check_obj(groups, expected_groups)

    def test_get_group(self, tatlin, make_mock):
        # Mock get_group method
        group = {
            'name': 'admin',
            'gid': 1100,
            'displayName': 'Administrative group',
        }

        make_mock(target=OPEN_URL_FUNC, return_value=group)

        # Define expected data
        expected_group = {
            'name': 'admin',
            'gid': 1100,
            'comment': 'Administrative group',
        }

        # Get tatlin group
        group = tatlin.get_user_group('admin')

        # Result: Group with expected params was returned
        assert isinstance(group, UserGroup)
        check_obj(group, expected_group)

    def test_create_user_group(self, tatlin, make_mock, open_url_kwargs):
        # Mock get_group method
        make_mock(target=TATLIN_API_CLIENT_CLASS + '.get_user_group')

        # Mock open_url method
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Create user group
        tatlin.create_user_group(name='testgroup', comment='Test Group')

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}/{1}'.format(
                GROUPS_ENDPOINT, 'testgroup'),
            data=json.dumps({
                'displayName': 'Test Group',
                'memberOf': [],
            }),
            headers={'Content-Type': 'application/json'},
        )

        # Result: Request with expected parameters was sent to tatlin
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_group_not_found_after_creating(self, tatlin, make_mock):
        # Mock PUT request
        make_mock(target=REST_CLIENT_CLASS + '.put')

        # Mock not found error for open_url
        make_mock(
            target=OPEN_URL_FUNC,
            side_effect=RESTClientNotFoundError,
        )

        # Result: Correct exception was thrown by create_group
        with pytest.raises(TatlinClientError):
            tatlin.create_user_group(name='grouperror')

    def test_group_update(self, tatlin, make_mock, open_url_kwargs):
        # Mock reload method
        make_mock(target=USER_GROUP_CLASS + '.reload')

        # Mock open_url method
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Create group
        group = UserGroup(
            client=tatlin,
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

    def test_group_update_no_args(self, tatlin):
        # Create group
        group = UserGroup(
            client=tatlin,
            name='testgroup',
            gid=3000,
        )

        # Check if TypeError raises when group updates without parameters
        with pytest.raises(TypeError):
            group.update()

    def test_users(self, tatlin, make_mock):
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

        make_mock(
            target=OPEN_URL_FUNC,
            return_value={
                'first_user': first_user,
                'second_user': second_user,
            },
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
        group = UserGroup(client=tatlin, name='testname', gid=2000)

        # Result: 2 users with expected params was returned
        assert len(group.users) == 2
        check_obj(group.users, expected_users)

    def test_delete(self, tatlin, make_mock, open_url_kwargs):
        # Mock open_url
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Create group
        group = UserGroup(
            client=tatlin,
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

    def test_parent_groups(self, tatlin, make_mock):
        # Mock reload method
        make_mock(target=USER_GROUP_CLASS + '.reload')

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

        make_mock(OPEN_URL_FUNC, return_value=[data, monitor, testgroup])

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
            client=tatlin,
            name='testgroup',
            gid=2001,
            member_of=[{'name': 'data'}, {'name': 'monitor'}],
        )

        # Result: 2 parent groups with expected params was returned
        assert len(group.parent_groups) == 2
        check_obj(group.parent_groups, expected_groups)
