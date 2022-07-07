# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
from hamcrest import assert_that, has_entries
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.auth.ldap_config import LdapConfig
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import (
    OPEN_URL_FUNC,
    LDAP_CONFIG_CLASS,
)


class TestLdapConfig:

    def test_new_ldap_config(
        self, client, mock_method, open_url_kwargs, mocker
    ):
        # Mock load method
        mock_method(target=LDAP_CONFIG_CLASS + '.load')

        # Mock open_url method
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Create LDAP config object
        ldap_config = LdapConfig(client=client)

        # Update LDAP config
        ldap_config.update(
            host='127.0.0.1',
            port=636,
            lookup_user='LookupUser',
            lookup_password='***REMOVED***',
            base_dn='dc=yadro,dc=com',
            search_filter='(memberof=cn=TestUsers,dc=yadro,dc=com)',
            encryption='tls',
            cert='testcert',
            user_attribute='sAMAccountName',
            group_attribute='cn',
            type='custom',
        )

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(
                client.auth_service.LDAP_CONFIG_ENDOPINT),
            data=mocker.ANY,
            headers={'Content-Type': 'application/json'},
        )

        # Result: Request with expected parameters was sent to tatlin
        open_url_mock.assert_called_with(**open_url_kwargs)

        # Satisfy Python 2. It does not have builtin dict order,
        # so resulting json may be in different order than expected
        call_args, call_kwargs = open_url_mock.call_args
        call_data = json.loads(call_kwargs['data'])
        expected_call_data = {
            'host': '127.0.0.1',
            'port': '636',
            'lookUpUserName': 'LookupUser',
            'lookUpUserPwd': '***REMOVED***',
            'usersFilter': '(memberof=cn=TestUsers,dc=yadro,dc=com)',
            'baseDn': 'dc=yadro,dc=com',
            'attrLogin': 'sAMAccountName',
            'attrGroup': 'cn',
            'type': 'custom',
            'useStartTls': True,
            'useSsl': False,
            'rootCa': 'testcert',
        }
        assert_that(call_data, has_entries(expected_call_data))

    def test_update_existing_ldap_config(
        self, client, mock_method, open_url_kwargs, mocker,
    ):
        # Mock load method
        mock_method(target=LDAP_CONFIG_CLASS + '.load')

        # Mock open_url method
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Create LDAP config object
        ldap_config = LdapConfig(client=client)
        ldap_config.host = '127.0.0.1'
        ldap_config.port = '636'
        ldap_config.lookup_user = 'LookupUser'
        ldap_config.base_dn = 'dc=yadro,dc=com'
        ldap_config.encryption = 'tls'
        ldap_config.user_attribute = 'sAMAccountName'
        ldap_config.group_attribute = 'cn'
        ldap_config.type = 'custom'

        # Update search filter for LDAP
        ldap_config.update(
            lookup_password='***REMOVED***',
            search_filter='(memberof=cn=TestUsers,dc=yadro,dc=com)',
            cert='testcert',
        )

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(
                client.auth_service.LDAP_CONFIG_ENDOPINT),
            data=mocker.ANY,
            headers={'Content-Type': 'application/json'},
        )

        # Result: Request with expected parameters was sent to tatlin
        open_url_mock.assert_called_with(**open_url_kwargs)

        # Satisfy Python 2. It does not have builtin dict order,
        # so resulting json may be in different order than expected
        call_args, call_kwargs = open_url_mock.call_args
        call_data = json.loads(call_kwargs['data'])
        expected_call_data = {
            'host': '127.0.0.1',
            'port': '636',
            'lookUpUserName': 'LookupUser',
            'lookUpUserPwd': '***REMOVED***',
            'usersFilter': '(memberof=cn=TestUsers,dc=yadro,dc=com)',
            'baseDn': 'dc=yadro,dc=com',
            'attrLogin': 'sAMAccountName',
            'attrGroup': 'cn',
            'type': 'custom',
            'useStartTls': True,
            'useSsl': False,
            'rootCa': 'testcert',
        }
        assert_that(call_data, has_entries(expected_call_data))

    def test_reset_ldap(self, client, mock_method, open_url_kwargs):
        # Mock load method
        mock_method(target=LDAP_CONFIG_CLASS + '.load')

        # Mock open_url method
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Create LDAP config object
        ldap_config = LdapConfig(client=client)

        # Reset LDAP config
        ldap_config.reset()

        # Defining expected call parameters
        open_url_kwargs.update(
            method='DELETE',
            url='https://localhost/{0}'.format(
                client.auth_service.LDAP_CONFIG_ENDOPINT),
        )

        # Result: Request with expected parameters was sent to tatlin"):
        open_url_mock.assert_called_with(**open_url_kwargs)
