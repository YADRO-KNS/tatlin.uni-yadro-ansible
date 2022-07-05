# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.auth.ldap_config import LdapConfig


class TestLdapConfig:

    def test_new_ldap_config(self, client, update_ldap_mock, open_url_kwargs):
        ldap_config = LdapConfig(client=client)

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

        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(
                client.auth_service.LDAP_CONFIG_ENDOPINT),
            data=json.dumps({
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
            }),
            headers={'Content-Type': 'application/json'},
        )

        update_ldap_mock.assert_called_with(**open_url_kwargs)

    def test_update_existing_ldap_config(
        self, client, update_ldap_mock, open_url_kwargs
    ):
        ldap_config = LdapConfig(client=client)
        ldap_config.host = '127.0.0.1'
        ldap_config.port = '636'
        ldap_config.lookup_user = 'LookupUser'
        ldap_config.base_dn = 'dc=yadro,dc=com'
        ldap_config.encryption = 'tls'
        ldap_config.user_attribute = 'sAMAccountName'
        ldap_config.group_attribute = 'cn'
        ldap_config.type = 'custom'

        ldap_config.update(
            lookup_password='***REMOVED***',
            search_filter='(memberof=cn=TestUsers,dc=yadro,dc=com)',
            cert='testcert',
        )

        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(
                client.auth_service.LDAP_CONFIG_ENDOPINT),
            data=json.dumps({
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
            }),
            headers={'Content-Type': 'application/json'},
        )

        update_ldap_mock.assert_called_with(**open_url_kwargs)

    def test_reset_ldap(self, client, reset_ldap_mock, open_url_kwargs):
        ldap_config = LdapConfig(client=client)
        ldap_config.reset()
        open_url_kwargs.update(
            method='DELETE',
            url='https://localhost/{0}'.format(
                client.auth_service.LDAP_CONFIG_ENDOPINT),
        )
        reset_ldap_mock.assert_called_with(**open_url_kwargs)
