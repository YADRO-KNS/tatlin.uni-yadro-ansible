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


class TestGroup:

    def test_group_update(self, client, update_group_mock, open_url_kwargs):
        group = UserGroup(
            client=client,
            name='testgroup',
            gid=3000,
        )

        group.update(comment='testcomment')

        open_url_kwargs.update(
            method='POST',
            url='https://localhost/{0}/{1}'.format(
                client.auth_service.GROUPS_ENDPOINT, 'testgroup'),
            data=json.dumps({
                'displayName': 'testcomment',
                'memberOf': []
            }),
            headers={'Content-Type': 'application/json'},
        )

        update_group_mock.assert_called_with(**open_url_kwargs)

    def test_group_update_no_args(self, client):
        group = UserGroup(
            client=client,
            name='testgroup',
            gid=3000,
        )

        with pytest.raises(TypeError):
            group.update()

    def test_users(self, client, group_users_mock):
        expected_users = [
            dict(name='first_user',
                 enabled=True,
                 uid=1100,),
            dict(name='second_user',
                 enabled=False,
                 uid=2000)]

        group = UserGroup(client=client, name='testname', gid=2000)

        for user in group.users:
            check_object(user, expected_users)

    def test_delete(self, client, delete_group_mock, open_url_kwargs):
        group = UserGroup(
            client=client,
            name='testgroup',
            gid=3000,
        )

        group.delete()

        open_url_kwargs.update(
            method='DELETE',
            url='https://localhost/{0}/{1}'.format(
                client.auth_service.GROUPS_ENDPOINT, 'testgroup'),
        )

        delete_group_mock.assert_called_with(**open_url_kwargs)

    def test_parent_groups(self, client, parent_groups_mock):
        expected_groups = [
            dict(name='data',
                 gid=1513,
                 comment='Data users'),
            dict(name='monitor',
                 gid=1013,
                 comment='Users with monitoring permissions')]

        group = UserGroup(
            client=client,
            name='testgroup',
            gid=2001,
            member_of=[{'name': 'data'}, {'name': 'monitor'}],
        )

        assert len(group.parent_groups) == 2
        for group in group.parent_groups:
            check_object(group, expected_groups)
