# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
from hamcrest import assert_that, has_entries
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.models.ldap import LdapConfig
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import LDAP_CONFIG_ENDOPINT
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import check_obj
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import (
    OPEN_URL_FUNC, LDAP_CONFIG_CLASS,
)


class TestLdapConfig:

    def test_get_ldap_config(self, tatlin, make_mock):
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

        make_mock(target=OPEN_URL_FUNC, return_value=ldap_config)

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
        ldap_config = tatlin.get_ldap_config()

        # Result: LDAP config with expected params was returned
        check_obj(ldap_config, expected_config)

    def test_new_ldap_config(
        self, tatlin, make_mock, open_url_kwargs, mocker
    ):
        # Mock load method
        make_mock(target=LDAP_CONFIG_CLASS + '.load')

        # Mock open_url method
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Create LDAP config object
        ldap_config = LdapConfig(client=tatlin)

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
            url='https://localhost/{0}'.format(LDAP_CONFIG_ENDOPINT),
            data=mocker.ANY,
            headers={'Content-Type': 'application/json'},
        )

        # Result: Request with expected parameters was sent to tatlin
        open_url_mock.assert_called_with(**open_url_kwargs)

        # Satisfy Python <= 2.7 & 3.5. It does not have builtin dict order,
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
        self, tatlin, make_mock, open_url_kwargs, mocker,
    ):
        # Mock load method
        make_mock(target=LDAP_CONFIG_CLASS + '.load')

        # Mock open_url method
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Create LDAP config object
        ldap_config = LdapConfig(client=tatlin)
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
            url='https://localhost/{0}'.format(LDAP_CONFIG_ENDOPINT),
            data=mocker.ANY,
            headers={'Content-Type': 'application/json'},
        )

        # Result: Request with expected parameters was sent to tatlin
        open_url_mock.assert_called_with(**open_url_kwargs)

        # Satisfy Python <= 2.7 & 3.5. It does not have builtin dict order,
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

    def test_reset_ldap(self, tatlin, make_mock, open_url_kwargs):
        # Mock load method
        make_mock(target=LDAP_CONFIG_CLASS + '.load')

        # Mock open_url method
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Create LDAP config object
        ldap_config = LdapConfig(client=tatlin)

        # Reset LDAP config
        ldap_config.reset()

        # Defining expected call parameters
        open_url_kwargs.update(
            method='DELETE',
            url='https://localhost/{0}'.format(LDAP_CONFIG_ENDOPINT),
        )

        # Result: Request with expected parameters was sent to tatlin"):
        open_url_mock.assert_called_with(**open_url_kwargs)
