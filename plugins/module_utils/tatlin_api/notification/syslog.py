# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import SYSLOG_ENDPOINT
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError

try:
    from typing import Dict, Union, Optional
except ImportError:
    Dict = Union = Optional = None


class SyslogConfig:

    def __init__(self, client):
        self._client = client
        self.recipients = []
        self._endpoint = SYSLOG_ENDPOINT

        self.load()

    def load(self):  # type: () -> None
        data = self._client.get(self._endpoint).json

        loaded_recipients = []
        for recipient, params in data.get('recipients', {}).items():
            address, port = recipient.split(':')
            loaded_recipients.append({
                'address': address,
                'port': port,
                'protocol': params.get('protocol'),
                'facility': params.get('facility'),
                'severity': params.get('severity'),
                'audit': params.get('audit'),
            })

        self.recipients = loaded_recipients

    def add_recipient(
        self,
        address,  # type: str
        port,  # type: Union[str, int]
        protocol,  # type: str
        facility,  # type: int
        severity,  # type: str
        audit,  # type: bool
    ):
        self.set_recipients(self.recipients + [{
            'address': address,
            'port': port,
            'protocol': protocol,
            'facility': facility,
            'severity': severity,
            'audit': audit,
        }])

    def get_recipient(self, address, port):
        # type: (str, Union[str, int]) -> Optional[Dict]

        port = str(port)
        for recipient in self.recipients:
            if recipient['address'] == address and recipient['port'] == port:
                return recipient

    def remove_recipient(self, address, port):
        # type: (str, Union[str, int]) -> None

        port = str(port)
        new_recipients = []

        for recipient in self.recipients:
            need_remove = all([
                recipient['address'] == address,
                recipient['port'] == port
            ])

            if not need_remove:
                new_recipients.append(recipient)

        self.set_recipients(new_recipients)

    def reset(self):  # type: () -> None
        self._client.delete(self._endpoint + '/configuration')
        self.load()

    def set_recipients(self, recipients):
        body_recipients = {}
        for recipient in recipients:
            self.validate_recipient(recipient)

            recipient_id = ':'.join(
                [recipient['address'], str(recipient['port'])]
            )

            body_recipients[recipient_id] = {
                'protocol': recipient['protocol'],
                'facility': recipient['facility'],
                'severity': recipient['severity'].upper(),
                'audit': recipient['audit'],
            }

        self._client.put(self._endpoint, body={'recipients': body_recipients})

        self.load()

    @staticmethod
    def validate_recipient(recipient):  # type: (Dict) -> None
        valid_keys = (
            'address',
            'port',
            'protocol',
            'facility',
            'severity',
            'audit',
        )

        missing_keys = []
        for key in valid_keys:
            if key not in recipient:
                missing_keys.append(key)

        if len(missing_keys) > 0:
            raise TatlinClientError(
                'Missing expected recipient fields: {0}'.format(
                    ', '.join(missing_keys))
            )

        unexpected_keys = []
        for key in recipient.keys():
            if key not in valid_keys:
                unexpected_keys.append(key)

        if len(unexpected_keys) > 0:
            raise TatlinClientError(
                'Unexpected recipient fields: {0}'.format(
                    ', '.join(unexpected_keys))
            )

        try:
            int(recipient['port'])
        except ValueError:
            raise TatlinClientError(
                'Wrong value for port {0}'.format(recipient['port'])
            )
