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
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.auth.user import User
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.auth.group import UserGroup


class TestUser:

    def test_user_update(self, client, update_user_mock, open_url_kwargs):
        user = User(
            client=client,
            name='testuser',
            uid=11111,
            enabled=False,
            member_of=['testuser'],
        )

        user.update(
            password='123',
            enabled=True,
            groups=[
                'admin',
                UserGroup(client=client, name='testgroup', gid=2001),
            ],
        )

        open_url_kwargs.update(
            method='POST',
            url='https://localhost/{0}/{1}'.format(
                client.auth_service.USERS_ENDPOINT, 'testuser'),
            data=json.dumps({
                'enabled': 'true',
                'secret': '123',
                'memberOf': ['admin', 'testgroup'],
            }),
            headers={'Content-Type': 'application/json'},
        )

        update_user_mock.assert_called_with(**open_url_kwargs)

    def test_update_one_argument(
        self, client, update_user_mock, open_url_kwargs
    ):
        user = User(
            client=client,
            name='testuser',
            uid=11111,
            enabled=True,
            member_of=['testuser'],
        )

        user.update(enabled=False)

        open_url_kwargs.update(
            method='POST',
            url='https://localhost/{0}/{1}'.format(
                client.auth_service.USERS_ENDPOINT, 'testuser'),
            data=json.dumps({
                'enabled': 'false',
            }),
            headers={'Content-Type': 'application/json'},
        )

        update_user_mock.assert_called_with(**open_url_kwargs)

    def test_update_no_arguments(self, client):
        user = User(
            client=client,
            name='testuser',
            uid=11111,
            enabled=True,
            member_of=['testuser'],
        )

        with pytest.raises(TypeError):
            user.update()

    def test_groups(self, client, user_groups_mock):
        expected_groups = [
            dict(name='admin',
                 gid=1100,
                 comment='Administrative group'),
            dict(name='testuser',
                 gid=2001,
                 comment='')]

        user = User(
            client=client,
            name='testuser',
            uid=11111,
            enabled=True,
            member_of=['testuser', 'admin'],
        )

        for group in user.groups:
            check_object(group, expected_groups)

    def test_delete(self, client, delete_user_mock, open_url_kwargs):
        user = User(
            client=client,
            name='testuser',
            uid=11111,
            enabled=True,
            member_of=['testuser'],
        )

        user.delete()

        open_url_kwargs.update(
            method='DELETE',
            url='https://localhost/{0}/{1}'.format(
                client.auth_service.USERS_ENDPOINT, 'testuser'),
        )

        delete_user_mock.assert_called_with(**open_url_kwargs)
