# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import pytest
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import check_obj
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.auth.user import User
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.auth.group import UserGroup
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import (
    USERS_ENDPOINT, GROUPS_ENDPOINT,
)
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import (
    TatlinClientError, RESTClientNotFoundError,
)
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import (
    OPEN_URL_FUNC,
    AUTH_SERVICE_CLASS,
    REST_CLIENT_CLASS,
)


class TestAuthService:

    def test_get_users(self, client, mock_method):
        # Mock get_users method with 2 users
        mock_method(
            target=OPEN_URL_FUNC,
            admin={
                'name': 'admin',
                'enabled': True,
                'uid': 1100,
                'memberOf': ['admin'],
            },
            testuser={
                'name': 'testuser',
                'enabled': False,
                'uid': 2000,
                'memberOf': ['testuser', 'admin'],
            }
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
        users = client.auth_service.get_users()

        # Result: 2 users with expected params was returned
        assert len(users) == 2
        check_obj(users, expected_users)

    def test_get_user(self, client, mock_method):
        # Mock get_user method
        user = {
            'name': 'admin',
            'enabled': True,
            'uid': 1100,
            'memberOf': ['admin'],
        }

        mock_method(target=OPEN_URL_FUNC, **user)

        # Define expected data
        expected_user = {
            'name': 'admin',
            'enabled': True,
            'uid': 1100,
        }

        # Get tatlin user
        user = client.auth_service.get_user('admin')

        # User with expected params was returned
        assert isinstance(user, User)
        check_obj(user, expected_user)

    def test_create_user(self, client, mock_method, open_url_kwargs):
        # Mock get_users method with two users
        mock_method(target=AUTH_SERVICE_CLASS + '.get_user')
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Create tatlin user
        client.auth_service.create_user(
            name='testname',
            password='password',
            groups=[
                'monitor',
                UserGroup(client=client, name='data', gid=2000)
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

    def test_user_not_found_after_creating(self, client, mock_method):
        # Mock PUT request
        mock_method(target=REST_CLIENT_CLASS + '.put')

        # Mock not found error for open_url"):
        mock_method(
            target=OPEN_URL_FUNC,
            side_effects=RESTClientNotFoundError,
        )

        # Result: Correct exception was thrown by create_user
        with pytest.raises(TatlinClientError):
            client.auth_service.create_user(
                name='usererror', password='pass',
                groups=UserGroup(client=client, name='testgroup', gid=2000)
            )

    def test_get_groups(self, client, mock_method):
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

        mock_method(OPEN_URL_FUNC, admin, testgroup)

        # Define expected data
        expected_groups = [
            dict(name='admin',
                 gid=1100,
                 comment='Administrative group'),
            dict(name='testgroup',
                 gid=2001,
                 comment='')]

        # Get all tatlin groups
        groups = client.auth_service.get_groups()

        # Result: 2 groups with expected params was returned
        assert len(groups) == 2
        check_obj(groups, expected_groups)

    def test_get_group(self, client, mock_method):
        # Mock get_group method
        group = {
            'name': 'admin',
            'gid': 1100,
            'displayName': 'Administrative group',
        }

        mock_method(target=OPEN_URL_FUNC, **group)

        # Define expected data
        expected_group = {
            'name': 'admin',
            'gid': 1100,
            'comment': 'Administrative group',
        }

        # Get tatlin group
        group = client.auth_service.get_group('admin')

        # Result: Group with expected params was returned
        assert isinstance(group, UserGroup)
        check_obj(group, expected_group)

    def test_create_group(self, client, mock_method, open_url_kwargs):
        # Mock get_group method
        mock_method(target=AUTH_SERVICE_CLASS + '.get_group')

        # Mock open_url method
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Create tatlin group
        client.auth_service.create_group(
            name='testgroup', comment='Test Group')

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

    def test_group_not_found_after_creating(self, client, mock_method):
        # Mock PUT request
        mock_method(target=REST_CLIENT_CLASS + '.put')

        # Mock not found error for open_url
        mock_method(
            target=OPEN_URL_FUNC,
            side_effects=RESTClientNotFoundError,
        )

        # Result: Correct exception was thrown by create_group
        with pytest.raises(TatlinClientError):
            client.auth_service.create_group(name='grouperror')

    def test_get_ldap_config(self, client, mock_method):
        # Mock open_url method
        ldap_config = {
            'host': '127.0.0.1',
            'port': '389',
            'lookUpUserName': 'TestLookupUser',
            'baseDn': 'dc=yadro,dc=com',
            'userBaseDn': '',
            'groupBaseDn': '',
            'usersFilter': '(memberof=cn=Users,dc=yadro,dc=com)',
            'groupsFilter': '',
            'attrLogin': 'cn',
            'attrGroup': 'cn',
            'useSsl': True,
            'useStartTls': False,
            'type': 'custom',
        }

        mock_method(target=OPEN_URL_FUNC, **ldap_config)

        # Define expected parameters
        expected_config = {
            'host': '127.0.0.1',
            'port': '389',
            'lookup_user': 'TestLookupUser',
            'base_dn': 'dc=yadro,dc=com',
            'search_filter': '(memberof=cn=Users,dc=yadro,dc=com)',
            'encryption': 'ssl',
            'user_attribute': 'cn',
            'group_attribute': 'cn',
            'type': 'custom',
        }

        # Get LDAP config
        ldap_config = client.auth_service.get_ldap_config()

        # Result: LDAP config with expected params was returned
        check_obj(ldap_config, expected_config)
