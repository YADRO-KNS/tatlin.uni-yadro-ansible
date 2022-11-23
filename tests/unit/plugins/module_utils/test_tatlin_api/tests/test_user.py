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
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.models.user import User
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.models.user_group import UserGroup
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.endpoints import USERS_ENDPOINT
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.exception import (
    TatlinClientError, RESTClientNotFoundError,
)
from ansible_collections.yadro.tatlin_uni.tests.unit.plugins.module_utils.test_tatlin_api.constants import (
    OPEN_URL_FUNC, USER_CLASS, TATLIN_API_CLIENT_CLASS, REST_CLIENT_CLASS,
)


class TestUser:

    def test_get_users(self, tatlin, make_mock):
        # Mock get_users method with 2 users
        admin = {
            'name': 'admin',
            'enabled': True,
            'uid': 1100,
            'memberOf': ['admin'],
        }

        testuser = {
            'name': 'testuser',
            'enabled': False,
            'uid': 2000,
            'memberOf': ['testuser', 'admin'],
        }

        make_mock(
            target=OPEN_URL_FUNC,
            return_value={'admin': admin, 'testuser': testuser}
        )

        # Define expected data
        expected_users = [
            dict(name='admin',
                 enabled=True,
                 uid=1100),
            dict(name='testuser',
                 enabled=False,
                 uid=2000)]

        # Get all users
        users = tatlin.get_users()

        # Result: 2 users with expected params was returned
        assert len(users) == 2
        check_obj(users, expected_users)

    def test_get_user(self, tatlin, make_mock):
        # Mock get_user method
        user = {
            'name': 'admin',
            'enabled': True,
            'uid': 1100,
            'memberOf': ['admin'],
        }

        make_mock(target=OPEN_URL_FUNC, return_value=user)

        # Define expected data
        expected_user = {
            'name': 'admin',
            'enabled': True,
            'uid': 1100,
        }

        # Get tatlin user
        user = tatlin.get_user('admin')

        # User with expected params was returned
        assert isinstance(user, User)
        check_obj(user, expected_user)

    def test_create_user(self, tatlin, make_mock, open_url_kwargs):
        # Mock get_users method with two users
        make_mock(target=TATLIN_API_CLIENT_CLASS + '.get_user')
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Create tatlin user
        tatlin.create_user(
            name='testname',
            password='password',
            groups=[
                'monitor',
                UserGroup(client=tatlin, name='data', gid=2000)
            ]
        )

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}/{1}'.format(
                USERS_ENDPOINT, 'testname'),
            data=json.dumps({
                'secret': 'password',
                'memberOf': ['monitor', 'data'],
                'enabled': 'true',
            }),
            headers={'Content-Type': 'application/json'},
        )

        # Result: Request with expected parameters was sent to tatlin
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_user_not_found_after_creating(self, tatlin, make_mock):
        # Mock PUT request
        make_mock(target=REST_CLIENT_CLASS + '.put')

        # Mock not found error for open_url"):
        make_mock(
            target=OPEN_URL_FUNC,
            side_effect=RESTClientNotFoundError,
        )

        # Result: Correct exception was thrown by create_user
        with pytest.raises(TatlinClientError):
            tatlin.create_user(
                name='usererror', password='pass',
                groups=UserGroup(client=tatlin, name='testgroup', gid=2000)
            )

    def test_user_update(self, tatlin, make_mock, open_url_kwargs):
        # Mock reload method
        make_mock(target=USER_CLASS + '.reload')

        # Mock open_url method
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Create user
        user = User(
            client=tatlin,
            name='testuser',
            uid=11111,
            enabled=False,
            member_of=['testuser'],
        )

        # Update user
        user.update(
            password='123',
            enabled=True,
            groups=[
                'admin',
                UserGroup(client=tatlin, name='testgroup', gid=2001),
            ],
        )

        # Defining expected call parameters
        open_url_kwargs.update(
            method='POST',
            url='https://localhost/{0}/{1}'.format(
                USERS_ENDPOINT, 'testuser'),
            data=json.dumps({
                'enabled': 'true',
                'secret': '123',
                'memberOf': ['admin', 'testgroup'],
            }),
            headers={'Content-Type': 'application/json'},
        )

        # Result: Request with expected parameters was sent to tatlin
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_update_one_argument(
        self, tatlin, make_mock, open_url_kwargs
    ):
        # Mock reload method
        make_mock(target=USER_CLASS + '.reload')

        # Mock open_url method
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Create user
        user = User(
            client=tatlin,
            name='testuser',
            uid=11111,
            enabled=True,
            member_of=['testuser'],
        )

        # Update user state
        user.update(enabled=False)

        # Defining expected call parameters
        open_url_kwargs.update(
            method='POST',
            url='https://localhost/{0}/{1}'.format(
                USERS_ENDPOINT, 'testuser'),
            data=json.dumps({
                'enabled': 'false',
            }),
            headers={'Content-Type': 'application/json'},
        )

        # Result: Request with expected parameters was sent to tatlin
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_update_no_arguments(self, tatlin):
        # Create user
        user = User(
            client=tatlin,
            name='testuser',
            uid=11111,
            enabled=True,
            member_of=['testuser'],
        )

        # Check if TypeError raises when group updates without parameters"):
        with pytest.raises(TypeError):
            user.update()

    def test_groups(self, tatlin, make_mock):
        # Mock reload method
        make_mock(target=USER_CLASS + '.reload')

        # Mock response with 3 groups
        admin = {
            'name': 'admin',
            'gid': 1100,
            'displayName': 'Administrative group',
        }
        testuser = {
            'name': 'testuser',
            'gid': 2001,
            'displayName': '',
        }
        another_group = {
            'name': 'another_group',
            'gid': 2002,
            'displayName': 'Another group',
        }

        make_mock(
            target=OPEN_URL_FUNC,
            return_value=[admin, testuser, another_group],
        )

        # Define expected data
        expected_groups = [
            dict(name='admin',
                 gid=1100,
                 comment='Administrative group'),
            dict(name='testuser',
                 gid=2001,
                 comment='')]

        # Create user
        user = User(
            client=tatlin,
            name='testuser',
            uid=11111,
            enabled=True,
            member_of=['testuser', 'admin'],
        )

        # Result: 2 groups with expected params was returned
        assert len(user.groups) == 2
        check_obj(user.groups, expected_groups)

    def test_delete(self, tatlin, make_mock, open_url_kwargs):
        # Mock open_url method
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Create user
        user = User(
            client=tatlin,
            name='testuser',
            uid=11111,
            enabled=True,
            member_of=['testuser'],
        )

        # Delete user
        user.delete()

        # Defining expected call parameters
        open_url_kwargs.update(
            method='DELETE',
            url='https://localhost/{0}/{1}'.format(
                USERS_ENDPOINT, 'testuser'),
        )

        # Result: Request with expected parameters was sent to tatlin
        open_url_mock.assert_called_with(**open_url_kwargs)
