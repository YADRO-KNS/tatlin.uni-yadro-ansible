# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    from typing import Optional, List, Union, Dict
except ImportError:
    Optional = List = Union = Dict = None


from base64 import b64encode
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.rest_client import (
    RestClient, AUTH_BASIC, AUTH_SESSION)
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.auth.ldap_config import LdapConfig
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.auth.group import UserGroup
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.auth.user import User
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.osmgr.dns import DnsConfig
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.osmgr.ntp import NtpConfig
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.osmgr.port import Port
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.notification.smtp import SmtpConfig
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.notification.snmp import SnmpConfig
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.notification.syslog import SyslogConfig
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import (
    TatlinClientError, TatlinNodeNotFoundError, RESTClientNotFoundError)
import ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints as eps


LOGIN_PATH = 'auth/login'
LOGOUT_PATH = 'auth/logout'
ISCSI_AUTH_TYPES = ('none', 'oneway', 'mutual')


class TatlinClient(RestClient):

    def __init__(
        self,
        base_url,  # type: str
        username=None,  # type: Optional[str]
        password=None,  # type: Optional[str]
        validate_certs=True,  # type: Optional[bool]
        login_path=LOGIN_PATH,  # type: Optional[str]
        timeout=60,  # type: Optional[int]
        auth_method=AUTH_SESSION,  # type: Optional[str]
    ):  # type: (...) -> None

        super(TatlinClient, self).__init__(
            base_url=base_url,
            username=username,
            password=password,
            validate_certs=validate_certs,
            login_path=login_path,
            timeout=timeout,
            auth_method=auth_method,
        )

        self._ldap_config = None
        self._system_name = None
        self._system_version = None

    def __enter__(self):
        self.authorize(self._username, self._password, self._auth_method)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()

    def authorize(
        self,
        username=None,  # type: Optional[str]
        password=None,  # type: Optional[str]
        auth_method=None,  # type: Optional[str]
        login_path=None,  # type: Optional[str]
    ):  # type: (...) -> None

        self._username = username or self._username
        self._password = password or self._password
        self._auth_method = auth_method or self._auth_method
        self._login_path = login_path or self._login_path

        if self._auth_method == AUTH_BASIC:
            self._auth_key = 'Basic {0}'.format(b64encode(
                b':'.join((self._username, self._password))).strip())

        elif self._auth_method == AUTH_SESSION:
            if self._login_path is None:
                raise TatlinAuthorizationError(
                    'No login path was passed for session authorization'
                )

            response = self.post(
                self._login_path,
                body={'name': self._username, 'secret': self._password},
            ).json

            self._token = response['token']
        elif not self._auth_method:
            pass
        else:
            raise TatlinClientError(
                'Unrecognized authentication method ' + auth_method,
            )

    def create_user(
        self,
        name,  # type: str
        password,  # type: str
        groups,  # type: List[Union[str, UserGroup]]
        enabled=True,  # type: Optional[bool]
    ):  # type: (...) -> User

        groups = groups if isinstance(groups, list) else [groups]
        member_of = []
        for group in groups:
            member_of.append(group if isinstance(group, str) else group.name)

        self.put(
            eps.USERS_ENDPOINT + '/' + name,
            body={
                'secret': password,
                'memberOf': member_of,
                'enabled': 'true' if enabled else 'false',
            },
        )

        user = self.get_user(name)
        if user is None:
            raise TatlinClientError(
                'User {0} was not found after creation'.format(name)
            )

        return user

    def create_user_group(self, name, parent_groups=None, comment=None):
        # type: (str, List[Union[str, UserGroup]], str) -> UserGroup

        member_of = []
        if parent_groups is not None:
            parent_groups = parent_groups \
                if isinstance(parent_groups, list) \
                else [parent_groups]

            for parent in parent_groups:
                member_of.append({
                    'Name': parent if isinstance(parent, str) else parent.name
                })

        self.put(
            eps.GROUPS_ENDPOINT + '/' + name,
            body={
                'displayName': comment,
                'memberOf': member_of,
            }
        )

        group = self.get_user_group(name)
        if group is None:
            raise TatlinClientError(
                'Group {0} was not found after creation'.format(name)
            )

        return group

    def get_dns_config(self):
        return DnsConfig(client=self)

    def get_ldap_config(self):  # type: () -> LdapConfig
        if self._ldap_config is None:
            self._ldap_config = LdapConfig(self)
        self._ldap_config.load()
        return self._ldap_config

    def get_ntp_config(self):
        return NtpConfig(client=self)

    def get_port(self, name):  # type: (str) -> Port
        ports = self.get_ports()
        port = next((port for port in ports if port.name == name), None)

        if port is None:
            raise TatlinClientError(
                'Not found port with name {0}'.format(name),
            )

        return port

    def get_ports(self):  # type: () -> List[Port]
        rv = []
        ports_data = self.get(eps.PORTS_STATUS_ENDPOINT).json
        for port_data in ports_data:
            port = Port(client=self, port_data=port_data)
            rv.append(port)
        return rv

    def get_smtp_config(self):  # type: () -> SmtpConfig
        return SmtpConfig(client=self)

    def get_snmp_config(self):  # type: () -> SnmpConfig
        return SnmpConfig(client=self)

    def get_syslog_config(self):  # type: () -> SyslogConfig
        return SyslogConfig(client=self)

    def get_user(self, name):  # type: (str) -> Optional[User]
        try:
            data = self.get(eps.USERS_ENDPOINT + '/' + name).json
        except RESTClientNotFoundError:
            return None

        user = User(
            client=self,
            name=data['name'],
            uid=data['uid'],
            enabled=data['enabled'],
            member_of=data['memberOf'],
        )

        return user

    def get_users(self):  # type: () -> List[User]
        rv = []
        data = self.get(eps.USERS_ENDPOINT).json
        for item in data.values():
            user = User(
                client=self,
                name=item['name'],
                uid=item['uid'],
                enabled=item['enabled'],
                member_of=item['memberOf'],
            )
            rv.append(user)
        return rv

    def get_user_group(self, name):  # type: (str) -> Optional[UserGroup]
        try:
            data = self.get(eps.GROUPS_ENDPOINT + '/' + name).json
        except RESTClientNotFoundError:
            return None

        # Tatlin returns dict with empty name if group is not exist
        # instead of 404. It is not correct, but we have to handle this
        if not data.get('name'):
            return None

        group = UserGroup(
            client=self,
            name=data['name'],
            gid=data['gid'],
            comment=data.get('displayName'),
        )
        return group

    def get_user_groups(self):  # type: () -> List[UserGroup]
        rv = []
        data = self.get(eps.GROUPS_ENDPOINT).json

        for item in data:
            group = UserGroup(
                client=self,
                name=item['name'],
                gid=item['gid'],
                comment=item.get('displayName'),
            )
            rv.append(group)

        return rv

    def logout(self):  # type: () -> None
        if self._token:
            self.post(LOGOUT_PATH)

    def reboot_node(self, name):  # type: (str) -> None
        try:
            self.put(eps.REBOOT_ENDPOINT.format(node=name))
        except RESTClientNotFoundError:
            raise TatlinNodeNotFoundError(
                'Not found node with name {0}'.format(name)
            )

    # Potentially this method can have more arguments.
    # But now only one is needed
    def reconnect(self, host=None):
        self._host = host or self._host
        self.authorize()

    def set_iscsi_auth(
        self,
        auth,  # type: str
        username=None,  # type: str
        password=None,  # type: str
        mutual_username=None,  # type: str
        mutual_password=None,  # type: str
    ):
        if auth not in ISCSI_AUTH_TYPES:
            raise TatlinClientError(
                'Unknown iscsi auth type'
            )

        req_body = {'auth_type': auth}
        if auth in ('oneway', 'mutual'):
            if not username or not password:
                raise TatlinClientError(
                    'username and password must be provided '
                    'with auth type {0}'.format(auth)
                )

            req_body.update(internal_name=username,
                            internal_password=password)

        if auth == 'mutual':
            if not all([
                username, password, mutual_username, mutual_password
            ]):
                raise TatlinClientError(
                    'username, password, mutual_username and mutual_password '
                    'must be provided with {0} auth type'.format(auth)
                )

            req_body.update(external_name=mutual_username,
                            external_password=mutual_password)

        self.post(path=eps.PERSONALITIES_AUTH_ENDPOINT, body=req_body)

    def upload_ssl_certificate(self, crt, key):
        # type: (Union[str, bytes], Union[str, bytes]) -> None
        self.put(eps.CERTIFICATE_ENDPOINT, files={'crt': crt, 'key': key})

    @property
    def system_name(self):  # type: () -> str
        if self._system_name is None:
            self._system_name = self._get_system_name()
        return self._system_name

    @property
    def system_version(self):  # type: () -> str
        if self._system_version is None:
            self._system_version = self._get_system_version()
        return self._system_version

    def _get_system_name(self):
        data = self.get(eps.SYSTEM_NAME_ENDPOINT).json
        try:
            name = data['value']
        except (KeyError, TypeError):
            raise TatlinClientError('Failed to parse system name')
        return name

    def _get_system_version(self):
        data = self.get(eps.SYSTEM_VERSION_ENDPOINT).json
        try:
            version = data['tatlin-version']['L2']
        except (KeyError, TypeError):
            raise TatlinClientError('Failed to parse tatlin version')
        return version


class TatlinAuthorizationError(Exception):
    pass
