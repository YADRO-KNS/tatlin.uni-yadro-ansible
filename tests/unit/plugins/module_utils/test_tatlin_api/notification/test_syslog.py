# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.notification.syslog import SyslogConfig
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import SYSLOG_ENDPOINT
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import (
    check_obj, check_called_with)
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import (
    OPEN_URL_FUNC, SYSLOG_CONFIG_CLASS)


class TestSyslog:

    def test_get_syslog_config(self, tatlin, mock_method):
        # Mock open_url response with data
        mock_method(
            OPEN_URL_FUNC,
            recipients={
                '127.0.0.1:514': {
                    'protocol': 'udp',
                    'audit': False,
                    'facility': 21,
                    'severity': 'INFO'
                },
                'example.com:601': {
                    'protocol': 'tls',
                    'audit': True,
                    'facility': 11,
                    'severity': 'CRITICAL'
                },
            }
        )

        # Call get_syslog_config
        syslog_config = tatlin.get_syslog_config()

        # Define expected params
        exp_params = {'recipients': [
            dict(address='127.0.0.1',
                 port='514',
                 protocol='udp',
                 audit=False,
                 facility=21,
                 severity='INFO'),
            dict(address='example.com',
                 port='601',
                 protocol='tls',
                 audit=True,
                 facility=11,
                 severity='CRITICAL'),
        ]}

        # Result: Config with expected server was returned
        check_obj(syslog_config, exp_params, ignore_order='recipients')

    def test_load(self, tatlin, mock_method):
        # Save load method for future use
        init_load = SyslogConfig.load

        # Mock method load without data
        mock_method(target=SYSLOG_CONFIG_CLASS + '.load')

        # Create SyslogConfig object
        syslog_config = SyslogConfig(tatlin)

        # Ensure that config object has empty attributes
        check_obj(syslog_config, {'recipients': []})

        # Restore load method
        SyslogConfig.load = init_load

        # Mock open_url with data
        mock_method(
            OPEN_URL_FUNC,
            recipients={
                '127.0.0.1:514': {
                    'protocol': 'udp',
                    'audit': False,
                    'facility': 21,
                    'severity': 'INFO'
                },
                'example.com:601': {
                    'protocol': 'tls',
                    'audit': True,
                    'facility': 11,
                    'severity': 'CRITICAL'
                },
            }
        )

        # Load config
        syslog_config.load()

        # Define expected params
        exp_params = {'recipients': [
            dict(address='127.0.0.1',
                 port='514',
                 protocol='udp',
                 audit=False,
                 facility=21,
                 severity='INFO'),
            dict(address='example.com',
                 port='601',
                 protocol='tls',
                 audit=True,
                 facility=11,
                 severity='CRITICAL'),
        ]}

        # Result: Syslog config with expected parameters was returned
        check_obj(syslog_config, exp_params, ignore_order='recipients')

    def test_load_empty_data(self, tatlin, mock_method):
        # Save load method for future use
        init_load = SyslogConfig.load

        # Mock method load without data
        mock_method(target=SYSLOG_CONFIG_CLASS + '.load')

        # Create SyslogConfig object
        syslog_config = SyslogConfig(tatlin)

        # Ensure that config object has empty attributes
        check_obj(syslog_config, exp_params={'recipients': []})

        # Restore load method
        SyslogConfig.load = init_load

        # Mock open_url with data
        mock_method(OPEN_URL_FUNC)

        # Load config
        syslog_config.load()

        # Result: Syslog config with expected parameters was returned
        check_obj(syslog_config, exp_params={'recipients': []})

    def test_set_recipients(self, tatlin, mock_method, open_url_kwargs):
        # Mock open_url with data
        mock_method(
            OPEN_URL_FUNC,
            recipients={
                '127.1.1.1:1': {
                    'protocol': 'tcp',
                    'audit': True,
                    'facility': 1,
                    'severity': 'WARNING'
                },
            }
        )

        # Create SyslogConfig object
        syslog_config = tatlin.get_syslog_config()

        # Mock load method without data
        mock_method(SYSLOG_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Set recipients
        syslog_config.set_recipients(recipients=[
            dict(address='127.0.0.1',
                 port='514',
                 protocol='udp',
                 audit=False,
                 facility=21,
                 severity='INFO'),
            dict(address='example.com',
                 port='601',
                 protocol='tls',
                 audit=True,
                 facility=11,
                 severity='CRITICAL'),
        ])

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(SYSLOG_ENDPOINT),
            headers={'Content-Type': 'application/json'},
            data={
                'recipients': {
                    '127.0.0.1:514': {
                        'protocol': 'udp',
                        'audit': False,
                        'facility': 21,
                        'severity': 'INFO'
                    },
                    'example.com:601': {
                        'protocol': 'tls',
                        'audit': True,
                        'facility': 11,
                        'severity': 'CRITICAL'
                    },
                },
            },
        )

        # Result: open_url was called with expected params
        check_called_with(open_url_mock, **open_url_kwargs)

    def test_add_recipient(self, tatlin, mock_method, open_url_kwargs):
        # Mock open_url with data
        mock_method(
            OPEN_URL_FUNC,
            recipients={
                '127.0.0.1:514': {
                    'protocol': 'udp',
                    'audit': False,
                    'facility': 21,
                    'severity': 'INFO'
                },
            }
        )

        # Create SyslogConfig object
        syslog_config = tatlin.get_syslog_config()

        # Mock load method without data
        mock_method(SYSLOG_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Add recipient
        syslog_config.add_recipient(
            address='example.com',
            port='601',
            protocol='tls',
            audit=True,
            facility=11,
            severity='CRITICAL',
        )

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(SYSLOG_ENDPOINT),
            headers={'Content-Type': 'application/json'},
            data={
                'recipients': {
                    '127.0.0.1:514': {
                        'protocol': 'udp',
                        'audit': False,
                        'facility': 21,
                        'severity': 'INFO'
                    },
                    'example.com:601': {
                        'protocol': 'tls',
                        'audit': True,
                        'facility': 11,
                        'severity': 'CRITICAL'
                    },
                },
            },
        )

        # Result: open_url was called with expected params
        check_called_with(open_url_mock, **open_url_kwargs)

    @pytest.mark.parametrize(
        'address, port, result', [
            ('127.0.0.1', '514', dict(
                address='127.0.0.1',
                port='514',
                protocol='udp',
                audit=False,
                facility=21,
                severity='INFO'
            )),
            ('127.0.0.1', '515', None)
        ]
    )
    def test_get_recipient(self, tatlin, mock_method, address, port, result):
        # Mock open_url with data
        mock_method(
            OPEN_URL_FUNC,
            recipients={
                '127.0.0.1:514': {
                    'protocol': 'udp',
                    'audit': False,
                    'facility': 21,
                    'severity': 'INFO'
                },
                'example.com:601': {
                    'protocol': 'tls',
                    'audit': True,
                    'facility': 11,
                    'severity': 'CRITICAL'
                },
            }
        )

        # Create SyslogConfig object
        syslog_config = tatlin.get_syslog_config()

        # Request recipient
        recipient = syslog_config.get_recipient(address, port)

        # Result: Expected recipient was return
        assert recipient == result

    @pytest.mark.parametrize(
        'address, port, sent_recipients', [
            ('127.0.0.1', '514', {
                'example.com:514': dict(
                    protocol='tls',
                    audit=True,
                    facility=11,
                    severity='CRITICAL',
                )
            }),
            ('127.0.0.1', '515', {
                '127.0.0.1:514': dict(
                    protocol='udp',
                    audit=False,
                    facility=21,
                    severity='INFO',
                ),
                'example.com:514': dict(
                    protocol='tls',
                    audit=True,
                    facility=11,
                    severity='CRITICAL',
                )
            }),
        ]
    )
    def test_remove_recipient(
        self,
        tatlin,
        mock_method,
        open_url_kwargs,
        address,
        port,
        sent_recipients,
    ):
        # Mock open_url with data
        mock_method(
            OPEN_URL_FUNC,
            recipients={
                '127.0.0.1:514': {
                    'protocol': 'udp',
                    'audit': False,
                    'facility': 21,
                    'severity': 'INFO'
                },
                'example.com:514': {
                    'protocol': 'tls',
                    'audit': True,
                    'facility': 11,
                    'severity': 'CRITICAL'
                },
            }
        )

        # Create SyslogConfig object
        syslog_config = tatlin.get_syslog_config()

        # Mock load method without data
        mock_method(SYSLOG_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Remove recipient
        syslog_config.remove_recipient(address, port)

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(SYSLOG_ENDPOINT),
            headers={'Content-Type': 'application/json'},
            data={'recipients': sent_recipients},
        )

        # Result: open_url was called with expected params
        check_called_with(open_url_mock, **open_url_kwargs)

    def test_reset(self, tatlin, mock_method, open_url_kwargs):
        # Mock open_url with data
        mock_method(
            OPEN_URL_FUNC,
            recipients={
                '127.0.0.1:514': {
                    'protocol': 'udp',
                    'audit': False,
                    'facility': 21,
                    'severity': 'INFO'
                },
                'example.com:514': {
                    'protocol': 'tls',
                    'audit': True,
                    'facility': 11,
                    'severity': 'CRITICAL'
                },
            }
        )

        # Create SyslogConfig object
        syslog_config = tatlin.get_syslog_config()

        # Mock load method without data
        mock_method(SYSLOG_CONFIG_CLASS + '.load')

        # Mock open_url without data
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Reset config
        syslog_config.reset()

        # Defining expected call parameters
        open_url_kwargs.update(
            method='DELETE',
            url='https://localhost/{0}/configuration'.format(SYSLOG_ENDPOINT),
            data=None,
        )

        # Result: open_url was called with expected params
        check_called_with(open_url_mock, **open_url_kwargs)

    @pytest.mark.parametrize(
        'pop_param, new_param', [
            ('address', {}),
            ('port', {}),
            ('protocol', {}),
            ('facility', {}),
            ('severity', {}),
            ('audit', {}),
            ('', {'test_param': 'test_value'})
        ]
    )
    def test_set_invalid_recipient(
        self, tatlin, mock_method, pop_param, new_param,
    ):
        # Mock open_url with data
        mock_method(
            OPEN_URL_FUNC,
            recipients={
                '127.0.0.1:514': {
                    'protocol': 'udp',
                    'audit': False,
                    'facility': 21,
                    'severity': 'INFO'
                },
            }
        )

        # Create SyslogConfig object
        syslog_config = tatlin.get_syslog_config()

        # Mock load method without data
        mock_method(SYSLOG_CONFIG_CLASS + '.load')

        # Mock open_url without data
        mock_method(target=OPEN_URL_FUNC)

        # Define new recipient params
        recipient = dict(
            address='example.com',
            port='601',
            protocol='tls',
            audit=True,
            facility=11,
            severity='CRITICAL',
        )

        # Correct recipient params
        recipient.pop(pop_param, None)
        recipient.update(new_param)

        # Add invalid recipient
        with pytest.raises(TatlinClientError):
            syslog_config.set_recipients([recipient])
