# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    from typing import Optional, Dict
except ImportError:
    # Satisfy Python 2 which doesn't have typing.
    Optional = Dict = None

from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError


ENCRYPTION_TLS = 'tls'
ENCRYPTION_SSL = 'ssl'
ENCRYPTION_OFF = 'off'


class LdapConfig:

    def __init__(self, client):
        self._client = client
        self.host = None
        self.port = None
        self.lookup_user = None
        self.base_dn = None
        self.search_filter = None,
        self.encryption = None,
        self.user_attribute = None,
        self.group_attribute = None,
        self.type = None,

    def load(self):  # type: () -> None
        data = self._client.get(
            self._client.auth_service.LDAP_CONFIG_ENDOPINT,
        ).json

        self.host = data['host']
        self.port = data['port']
        self.lookup_user = data['lookUpUserName']
        self.base_dn = data['baseDn']
        self.search_filter = data['usersFilter']
        self.encryption = self._define_encryption(data)
        self.user_attribute = data['attrLogin']
        self.group_attribute = data['attrGroup']
        self.type = data['type']

    def _define_encryption(self, raw_data):  # type: (Dict) -> Optional[str]
        if raw_data['useSsl']:
            return ENCRYPTION_SSL
        elif raw_data['useStartTls']:
            return ENCRYPTION_TLS
        else:
            return ENCRYPTION_OFF

    def reset(self):
        self._client.delete(self._client.auth_service.LDAP_CONFIG_ENDOPINT)
        self.load()

    def update(self, lookup_password, **params):
        """
        Args:
            lookup_password (str): password for lookup user

        Keyword Args:
            host (str): Address of ldap server
            port (str): Ldap server's port
            lookup_user (str): Name of lookup user
            search_filter (str): Filter in RFC 4515 format.
                Example: '(memberof=CN=TatlinUsers,DC=example,DC=com)'
            base_dn (str): Base dn for search
            encryption (str): Encryption mode.
                Possible values: 'ssl', 'tls' or 'off'
            cert (str): Certificate content.
                Required when encryption is not 'off'
            user_attribute (str): Login attribute
            group_attribute (str): Group attribute
            type (str): Ldap server's type
        """

        if params.get('type', self.type) == 'ad':
            params['user_attribute'] = 'sAMAccountName'
            params['group_attribute'] = 'cn'

        request_body = {
            'host': params.get('host', self.host),
            'port': str(params.get('port', self.port)),
            'lookUpUserName': params.get('lookup_user', self.lookup_user),
            'lookUpUserPwd': lookup_password,
            'usersFilter': params.get('search_filter', self.search_filter),
            'baseDn': params.get('base_dn', self.base_dn),
            'attrLogin': params.get('user_attribute', self.user_attribute),
            'attrGroup': params.get('group_attribute', self.group_attribute),
            'type': params.get('type', self.type),
        }

        encryption = params.get('encryption', '').lower()
        if encryption and encryption != ENCRYPTION_OFF \
                and params.get('cert') is None:
            raise TatlinClientError(
                'Certificate must be passed when ssl '
                'or tls encryption is used'
            )
        elif encryption:
            if encryption == ENCRYPTION_TLS:
                request_body.update(
                    useStartTls=True, useSsl=False, rootCa=params['cert'],
                )
            elif encryption == ENCRYPTION_SSL:
                request_body.update(
                    useStartTls=False, useSsl=True, rootCa=params['cert'],
                )
            elif encryption == ENCRYPTION_OFF:
                request_body.update(useStartTls=False, useSsl=False)
            else:
                raise TatlinClientError(
                    'Unrecognized encryption mode {0}'.format(encryption)
                )
        else:
            request_body.update(
                useStartTls=(self.encryption == ENCRYPTION_TLS),
                useSsl=(self.encryption == ENCRYPTION_SSL),
                rootCa=params.get('cert'),
            )

        self._client.put(
            self._client.auth_service.LDAP_CONFIG_ENDOPINT,
            body=request_body,
        )

        self.load()
