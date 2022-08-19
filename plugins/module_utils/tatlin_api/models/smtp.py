# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    from typing import List
except ImportError:
    List = None

from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import SMTP_ENDPOINT


ENCRYPTION_TLS = 'tls'
ENCRYPTION_OFF = 'off'


class SmtpConfig:

    def __init__(self, client):
        self._client = client
        self.address = None
        self.port = None
        self.encryption = ENCRYPTION_OFF
        self.login = None
        self.sender = None
        self.recipients = []
        self._endpoint = SMTP_ENDPOINT

        self.load()

    def add_recipient(self, recipient):  # type: (str) -> None
        """
        Args:
             recipient: recipient's email
        """

        self.update(recipients=self.recipients + [recipient])

    def load(self):  # type: () -> None
        data = self._client.get(self._endpoint).json

        self.address = data.get('host')
        self.port = data.get('port')
        self.encryption = ENCRYPTION_TLS \
            if data.get('protocol') == ENCRYPTION_TLS else ENCRYPTION_OFF
        self.login = data.get('login', {}).get('username')
        self.sender = data.get('sender_email')
        self.recipients = list(r for r in data.get('recipients', {}).keys())

    def remove_recipient(self, recipient):  # type: (str) -> None
        """
        Args:
             recipient: recipient's email
        """
        self.update(recipients=[r for r in self.recipients if r != recipient])

    def reset(self):  # type: () -> None
        self._client.put(
            self._endpoint,
            body=None,
        )

        self.load()

    def update(
        self,
        address=None,  # type: str
        port=None,  # type: int
        encryption=None,  # type: str
        login=None,  # type: str
        password=None,  # type: str
        sender=None,  # type: str
        recipients=None,  # type: List[str]
    ):  # type: (...) -> None
        """
        Args:
            address: SMTP server's ip address or FQDN
            port: SMTP server's port
            encryption: Encryption protocol. Possible values: tls, off
            login: User's login
            password: User's password. Required if login is not None
            sender: An email, which will be used as sender for sent messages
            recipients: List of emails, messages receivers
        """

        request_body = {
            'host': address or self.address,
            'port': port or self.port,
            'sender_email': sender or self.sender,
        }

        if encryption in (ENCRYPTION_TLS, ENCRYPTION_OFF, None):
            protocol = encryption \
                if encryption is not None else self.encryption

            if protocol == ENCRYPTION_OFF:
                protocol = ''

            request_body['protocol'] = protocol
        else:
            raise TatlinClientError(
                'Unknown encryption type: {0}. Only {1} are supported'.format(
                    encryption, (ENCRYPTION_TLS, ENCRYPTION_OFF))
            )

        if login is not None or password is not None:
            if password is None:
                raise TatlinClientError(
                    'Password is None. If login is passed, '
                    'password is required',
                )

            request_body['login'] = {
                'username': login or self.login,
                'password': password,
            }

        if recipients is not None:
            request_body['recipients'] = dict((r, {}) for r in recipients)

        self._client.put(
            path=self._endpoint,
            body=request_body,
        )

        self.load()
