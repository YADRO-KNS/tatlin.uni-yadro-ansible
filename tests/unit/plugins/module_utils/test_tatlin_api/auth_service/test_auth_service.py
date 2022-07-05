# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import pytest
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import check_object
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.auth.user import User
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.auth.group import UserGroup
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError


class TestAuthService:

    def test_get_users(self, client, get_users_mock):
        expected_users = [
            dict(name='admin',
                 enabled=True,
                 uid=1100),
            dict(name='testuser',
                 enabled=False,
                 uid=2000)]

        users = client.auth_service.get_users()

        assert len(users) == 2
        for user in users:
            assert isinstance(user, User)
            check_object(user, expected_users)

    def test_get_user(self, client, get_user_mock):
        expected_user = {
            'name': 'admin',
            'enabled': True,
            'uid': 1100,
        }

        user = client.auth_service.get_user('admin')

        assert isinstance(user, User)
        check_object(user, expected_user)

    def test_create_user(self, client, create_user_mock, open_url_kwargs):
        client.auth_service.create_user(
            name='testname',
            password='password',
            groups=[
                'monitor',
                UserGroup(client=client, name='data', gid=2000)
            ]
        )

        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}/{1}'.format(
                client.auth_service.USERS_ENDPOINT, 'testname'),
            data=json.dumps({
                'secret': 'password',
                'memberOf': ['monitor', 'data'],
                'enabled': 'true',
            }),
            headers={'Content-Type': 'application/json'},
        )

        create_user_mock.assert_called_with(**open_url_kwargs)

    def test_user_not_found_after_creating(
        self, client, url_not_found_mock,
    ):
        with pytest.raises(TatlinClientError):
            client.auth_service.create_user(
                name='usererror', password='pass',
                groups=UserGroup(client=client, name='testgroup', gid=2000)
            )

    def test_get_groups(self, client, get_groups_mock):
        expected_groups = [
            dict(name='admin',
                 gid=1100,
                 comment='Administrative group'),
            dict(name='testgroup',
                 gid=2001,
                 comment='')]

        groups = client.auth_service.get_groups()

        assert len(groups) == 2
        for group in groups:
            assert isinstance(group, UserGroup)
            check_object(group, expected_groups)

    def test_get_group(self, client, get_group_mock):
        expected_group = {
            'name': 'admin',
            'gid': 1100,
            'comment': 'Administrative group',
        }

        group = client.auth_service.get_group('admin')

        assert isinstance(group, UserGroup)
        check_object(group, expected_group)

    def test_create_group(self, client, create_group_mock, open_url_kwargs):
        client.auth_service.create_group(
            name='testgroup', comment='Test Group')

        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}/{1}'.format(
                client.auth_service.GROUPS_ENDPOINT, 'testgroup'),
            data=json.dumps({
                'displayName': 'Test Group',
                'memberOf': [],
            }),
            headers={'Content-Type': 'application/json'},
        )

        create_group_mock.assert_called_with(**open_url_kwargs)

    def test_group_not_found_after_creating(
        self, client, url_not_found_mock,
    ):
        with pytest.raises(TatlinClientError):
            client.auth_service.create_group(name='grouperror')

    def test_get_ldap_config(self, client, get_ldap_mock):
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

        ldap_config = client.auth_service.get_ldap_config()
        check_object(ldap_config, expected_config)
