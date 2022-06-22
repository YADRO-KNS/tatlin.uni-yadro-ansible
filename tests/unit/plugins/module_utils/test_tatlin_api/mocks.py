# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import json
from ansible_collections.yadro.tatlin.tests.unit.compat.mock import MagicMock
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import RESTClientNotFoundError


REST_CLIENT_MODULE = 'ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.rest_client'
REST_CLIENT_CLASS = REST_CLIENT_MODULE + '.RestClient'
OPEN_URL_FUNC = REST_CLIENT_MODULE + '.open_url'
AUTH_PACKAGE = 'ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.auth'
AUTH_SERVICE_CLASS = AUTH_PACKAGE + '.auth_service.AuthService'
USER_CLASS = AUTH_PACKAGE + '.user.User'
USER_GROUP_CLASS = AUTH_PACKAGE + '.group.UserGroup'


def mock_response_data(
    mocker,
    *args,
    **kwargs
):

    # Python 2 does not support Keyword-Only Arguments (PEP 3102)
    side_effects = None
    target = OPEN_URL_FUNC
    if 'side_effects' in kwargs:
        side_effects = kwargs.pop('side_effects')
    if 'target' in kwargs:
        target = kwargs.pop('target')

    response_mock = MagicMock()
    response_mock.read.return_value = json.dumps(args or kwargs)

    mock = mocker.patch(
        target,
        side_effect=side_effects,
        return_value=response_mock,
    )

    return mock


@pytest.fixture
def url_not_found_mock(mocker):
    mock_response_data(
        mocker,
        target=REST_CLIENT_CLASS + '.put'
    )

    mock_response_data(mocker, side_effects=RESTClientNotFoundError)


@pytest.fixture
def get_users_mock(mocker):
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
        'memberOf': ['testuser', 'admin']
    }

    mock_response_data(mocker, admin=admin, testuser=testuser)


@pytest.fixture
def get_user_mock(mocker):
    user = {
        'name': 'admin',
        'enabled': True,
        'uid': 1100,
        'memberOf': ['admin'],
    }

    mock_response_data(mocker, **user)


@pytest.fixture
def create_user_mock(mocker):
    mock_response_data(
        mocker,
        target=AUTH_SERVICE_CLASS + '.get_user'
    )
    return mock_response_data(mocker)


@pytest.fixture
def update_user_mock(mocker):
    mock_response_data(mocker, target=USER_CLASS + '.reload')

    return mock_response_data(mocker)


@pytest.fixture
def delete_user_mock(mocker):
    return mock_response_data(mocker)


@pytest.fixture
def user_groups_mock(mocker):
    mock_response_data(mocker, target=USER_CLASS + '.reload')

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

    return mock_response_data(mocker, admin, testuser, another_group)


@pytest.fixture
def get_groups_mock(mocker):
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

    mock_response_data(mocker, admin, testgroup)


@pytest.fixture
def get_group_mock(mocker):
    group = {
        'name': 'admin',
        'gid': 1100,
        'displayName': 'Administrative group',
    }

    mock_response_data(mocker, **group)


@pytest.fixture
def create_group_mock(mocker):
    mock_response_data(
        mocker,
        target=AUTH_SERVICE_CLASS + '.get_group'
    )
    return mock_response_data(mocker)


@pytest.fixture
def update_group_mock(mocker):
    mock_response_data(
        mocker,
        target=USER_GROUP_CLASS + '.reload'
    )

    return mock_response_data(mocker)


@pytest.fixture
def delete_group_mock(mocker):
    return mock_response_data(mocker)


@pytest.fixture
def group_users_mock(mocker):

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

    return mock_response_data(
        mocker, first_user=first_user, second_user=second_user)


@pytest.fixture
def parent_groups_mock(mocker):
    mock_response_data(mocker, target=USER_GROUP_CLASS + '.reload')

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

    return mock_response_data(mocker, data, monitor, testgroup)
