# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import json
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import check_obj
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.auth.user import User
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.auth.group import UserGroup
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import USERS_ENDPOINT
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import (
    OPEN_URL_FUNC, USER_CLASS,
)


class TestUser:

    def test_user_update(self, client, mock_method, open_url_kwargs):
        # Mock reload method
        mock_method(target=USER_CLASS + '.reload')

        # Mock open_url method
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Create user
        user = User(
            client=client,
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
                UserGroup(client=client, name='testgroup', gid=2001),
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
        self, client, mock_method, open_url_kwargs
    ):
        # Mock reload method
        mock_method(target=USER_CLASS + '.reload')

        # Mock open_url method
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Create user
        user = User(
            client=client,
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

    def test_update_no_arguments(self, client):
        # Create user
        user = User(
            client=client,
            name='testuser',
            uid=11111,
            enabled=True,
            member_of=['testuser'],
        )

        # Check if TypeError raises when group updates without parameters"):
        with pytest.raises(TypeError):
            user.update()

    def test_groups(self, client, mock_method):
        # Mock reload method
        mock_method(target=USER_CLASS + '.reload')

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

        mock_method(OPEN_URL_FUNC, admin, testuser, another_group)

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
            client=client,
            name='testuser',
            uid=11111,
            enabled=True,
            member_of=['testuser', 'admin'],
        )

        # Result: 2 groups with expected params was returned
        assert len(user.groups) == 2
        check_obj(user.groups, expected_groups)

    def test_delete(self, client, mock_method, open_url_kwargs):
        # Mock open_url method
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Create user
        user = User(
            client=client,
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
