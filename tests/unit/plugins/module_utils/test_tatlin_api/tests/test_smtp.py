# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.models.smtp import SmtpConfig
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import SMTP_ENDPOINT
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import (
    check_obj, check_called_with,
)
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import (
    OPEN_URL_FUNC, SMTP_CONFIG_CLASS,
)


class TestSmtp:

    def test_get_smtp_config(self, tatlin, make_mock):
        # Mock open_url response with data
        make_mock(
            OPEN_URL_FUNC,
            return_value={
                'host': '127.0.0.1',
                'port': 25,
                'protocol': '',
                'login': {'username': 'user', 'password': 'userpass'},
                'sender_email': 'smtp@example.com',
                'recipients': {
                    'first@recipients.com': {},
                    'second@recipients.com': {},
                }
            }
        )

        # Call get_smtp_config
        smtp_config = tatlin.get_smtp_config()

        # Define expected params
        exp_params = {
            'address': '127.0.0.1',
            'port': 25,
            'encryption': 'off',
            'login': 'user',
            'sender': 'smtp@example.com',
            'recipients': ['first@recipients.com', 'second@recipients.com'],
        }

        # Result: Config with expected server was returned
        check_obj(smtp_config, exp_params, ignore_order='recipients')

    def test_load(self, tatlin, make_mock):
        # Save load method for future use
        init_load = SmtpConfig.load

        # Mock method load without data
        make_mock(target=SMTP_CONFIG_CLASS + '.load')

        # Create SmtpConfig object
        smtp_config = SmtpConfig(tatlin)

        # Ensure that config object has empty attributes
        check_obj(smtp_config, {
            'address': None,
            'port': None,
            'login': None,
            'encryption': 'off',
            'sender': None,
            'recipients': []
        })

        # Restore load method
        SmtpConfig.load = init_load

        # Mock open_url with data
        make_mock(
            OPEN_URL_FUNC,
            return_value={
                'host': 'example.com',
                'port': 587,
                'protocol': 'tls',
                'login': {'username': 'user', 'password': 'userpass'},
                'sender_email': 'smtp@example.com',
                'recipients': {
                    'first@recipients.com': {},
                    'second@recipients.com': {},
                    'third@recipients.com': {},
                }
            }
        )

        # Load config
        smtp_config.load()

        # Result: SMTP config with expected servers was returned
        check_obj(smtp_config, ignore_order='recipients', exp_params={
            'address': 'example.com',
            'port': 587,
            'encryption': 'tls',
            'login': 'user',
            'sender': 'smtp@example.com',
            'recipients': [
                'first@recipients.com',
                'second@recipients.com',
                'third@recipients.com',
            ],
        })

    def test_update_full(self, tatlin, make_mock, open_url_kwargs):
        # Mock open_url with data
        make_mock(
            OPEN_URL_FUNC,
            return_value={
                'host': 'example.com',
                'port': 587,
                'protocol': 'tls',
                'login': {'username': 'user', 'password': 'userpass'},
                'sender_email': 'smtp@example.com',
                'recipients': {
                    'first@recipients.com': {},
                    'second@recipients.com': {},
                }
            }
        )

        # Create SmtpConfig object
        smtp_config = tatlin.get_smtp_config()

        # Mock load method without data
        make_mock(SMTP_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Update config
        smtp_config.update(
            address='127.0.0.1',
            port=25,
            encryption='off',
            login='user',
            password='newpass',
            sender='newsender@example.com',
            recipients=['third@recipients.com'],
        )

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(SMTP_ENDPOINT),
            headers={'Content-Type': 'application/json'},
            data={
                'host': '127.0.0.1',
                'port': 25,
                'protocol': '',
                'login': {'username': 'user', 'password': 'newpass'},
                'sender_email': 'newsender@example.com',
                'recipients': {'third@recipients.com': {}}
            },
        )

        # Result: open_url was called with expected params
        check_called_with(open_url_mock, **open_url_kwargs)

    @pytest.mark.parametrize('init_protocol, new_encryption, sent_protocol', [
        ('', 'tls', 'tls'),
        ('tls', 'off', ''),
    ])
    def test_update_encryption(
        self,
        tatlin,
        make_mock,
        open_url_kwargs,
        init_protocol,
        new_encryption,
        sent_protocol,
    ):
        # Mock open_url with data
        make_mock(
            OPEN_URL_FUNC,
            return_value={
                'host': 'example.com',
                'port': 587,
                'protocol': init_protocol,
                'login': {'username': 'user', 'password': 'userpass'},
                'sender_email': 'smtp@example.com',
                'recipients': {
                    'first@recipients.com': {},
                    'second@recipients.com': {},
                }
            }
        )

        # Create SmtpConfig object
        smtp_config = tatlin.get_smtp_config()

        # Mock load method without data
        make_mock(SMTP_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Update encryption
        smtp_config.update(encryption=new_encryption)

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(SMTP_ENDPOINT),
            headers={'Content-Type': 'application/json'},
            data={
                'host': 'example.com',
                'port': 587,
                'protocol': sent_protocol,
                'sender_email': 'smtp@example.com',
            },
        )

        # Result: open_url was called with expected params
        check_called_with(open_url_mock, **open_url_kwargs)

    def test_update_login_without_password(self, tatlin, make_mock):
        # Mock open_url with data
        make_mock(
            OPEN_URL_FUNC,
            return_value={
                'host': 'example.com',
                'port': 587,
                'protocol': 'tls',
                'login': {'username': 'user', 'password': 'userpass'},
                'sender_email': 'smtp@example.com',
                'recipients': {
                    'first@recipients.com': {},
                    'second@recipients.com': {},
                }
            }
        )

        # Create SmtpConfig object
        smtp_config = tatlin.get_smtp_config()

        # Mock load method without data
        make_mock(SMTP_CONFIG_CLASS + '.load')

        # Mock open_url without data
        make_mock(target=OPEN_URL_FUNC)

        # Update login without password
        with pytest.raises(TatlinClientError) as exc_info:
            smtp_config.update(login='newuser')

        # Result: Exception with corresponding text was raised
        assert str(exc_info.value) == 'Password is None. If login is ' \
                                      'passed, password is required'

    def test_reset(self, tatlin, make_mock, open_url_kwargs):
        # Mock open_url with data
        make_mock(
            OPEN_URL_FUNC,
            return_value={
                'host': 'example.com',
                'port': 587,
                'protocol': 'tls',
                'login': {'username': 'user', 'password': 'userpass'},
                'sender_email': 'smtp@example.com',
                'recipients': {
                    'first@recipients.com': {},
                    'second@recipients.com': {},
                }
            }
        )

        # Create SmtpConfig object
        smtp_config = tatlin.get_smtp_config()

        # Mock load method without data
        make_mock(SMTP_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Reset Smtp config
        smtp_config.reset()

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(SMTP_ENDPOINT),
            data=None
        )

        # Result: open_url was called with expected params
        check_called_with(open_url_mock, **open_url_kwargs)

    def test_add_recipient(self, tatlin, make_mock, open_url_kwargs):
        # Mock open_url with data
        make_mock(
            OPEN_URL_FUNC,
            return_value={
                'host': 'example.com',
                'port': 587,
                'protocol': '',
                'login': {'username': 'user', 'password': 'userpass'},
                'sender_email': 'smtp@example.com',
                'recipients': {
                    'first@recipients.com': {},
                    'second@recipients.com': {},
                }
            }
        )

        # Create SmtpConfig object
        smtp_config = tatlin.get_smtp_config()

        # Mock load method without data
        make_mock(SMTP_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Add recipient
        smtp_config.add_recipient('third@recipients.com')

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(SMTP_ENDPOINT),
            headers={'Content-Type': 'application/json'},
            data={
                'host': 'example.com',
                'port': 587,
                'protocol': '',
                'sender_email': 'smtp@example.com',
                'recipients': {
                    'first@recipients.com': {},
                    'second@recipients.com': {},
                    'third@recipients.com': {},
                }
            },
        )

        # Result: open_url was called with expected params
        check_called_with(open_url_mock, **open_url_kwargs)

    def test_remove_recipient(self, tatlin, make_mock, open_url_kwargs):
        # Mock open_url with data
        make_mock(
            OPEN_URL_FUNC,
            return_value={
                'host': 'example.com',
                'port': 587,
                'protocol': '',
                'login': {'username': 'user', 'password': 'userpass'},
                'sender_email': 'smtp@example.com',
                'recipients': {
                    'first@recipients.com': {},
                    'second@recipients.com': {},
                    'third@recipients.com': {},
                }
            }
        )

        # Create SmtpConfig object
        smtp_config = tatlin.get_smtp_config()

        # Mock load method without data
        make_mock(SMTP_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Remove recipient
        smtp_config.remove_recipient('second@recipients.com')

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(SMTP_ENDPOINT),
            headers={'Content-Type': 'application/json'},
            data={
                'host': 'example.com',
                'port': 587,
                'protocol': '',
                'sender_email': 'smtp@example.com',
                'recipients': {
                    'first@recipients.com': {},
                    'third@recipients.com': {},
                }
            },
        )

        # Result: open_url was called with expected params
        check_called_with(open_url_mock, **open_url_kwargs)
