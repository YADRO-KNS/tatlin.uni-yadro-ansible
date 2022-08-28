# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import PERSONALITIES_AUTH_ENDPOINT
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import check_called_with
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import OPEN_URL_FUNC


class TestIscsiAuth:

    @pytest.mark.parametrize('auth_params, exp_data', [
        ({'auth': 'none'}, {'auth_type': 'none'}),
        ({'auth': 'oneway', 'username': 'user1', 'password': 'pass1'},
         {'auth_type': 'oneway',
          'internal_name': 'user1',
          'internal_password': 'pass1'}),
        ({'auth': 'mutual',
          'username': 'user2',
          'password': 'pass2',
          'mutual_username': 'user3',
          'mutual_password': 'pass3'},
         {'auth_type': 'mutual',
          'internal_name': 'user2',
          'internal_password': 'pass2',
          'external_name': 'user3',
          'external_password': 'pass3'})
    ])
    def test_set_iscsi_auth(
        self, tatlin, make_mock, open_url_kwargs, auth_params, exp_data,
    ):
        # Mock open_url without data
        open_url_mock = make_mock(OPEN_URL_FUNC)

        # Set iscsi auth
        tatlin.set_iscsi_auth(**auth_params)

        # Defining expected call parameters
        open_url_kwargs.update(
            method='POST',
            url='https://localhost/{0}'.format(PERSONALITIES_AUTH_ENDPOINT),
            data=exp_data,
            headers={'Content-Type': 'application/json'},
        )

        # Result: open_url was called with expected params
        check_called_with(open_url_mock, **open_url_kwargs)

    @pytest.mark.parametrize('auth_params', [
        {'auth': 'oneway'},
        {'auth': 'oneway', 'username': 'user1'},
        {'auth': 'oneway', 'password': 'pass1'},
        {'auth': 'mutual'},
        {'auth': 'mutual', 'username': 'user2'},
        {'auth': 'mutual', 'password': 'pass2'},
        {'auth': 'mutual', 'mutual_username': 'user3'},
        {'auth': 'mutual', 'mutual_password': 'pass3'},
        {'auth': 'mutual', 'username': 'user2', 'password': 'pass2'},
        {'auth': 'mutual', 'mutual_username': 'user3', 'mutual_password': 'pass3'}
    ])
    def test_set_iscsi_auth_missing_parameters(
        self, tatlin, make_mock, auth_params,
    ):
        # Mock open_url without data
        make_mock(OPEN_URL_FUNC)

        # Set iscsi auth
        # Result: TatlinClientError was raised
        with pytest.raises(TatlinClientError):
            tatlin.set_iscsi_auth(**auth_params)

    def test_set_iscsi_auth_wrong_auth_type(
        self, tatlin, make_mock,
    ):
        # Mock open_url without data
        make_mock(OPEN_URL_FUNC)

        # Set iscsi auth
        # Result: TatlinClientError was raised
        with pytest.raises(TatlinClientError):
            tatlin.set_iscsi_auth(auth='wrong_auth')
