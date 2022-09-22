# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints as eps
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.models.subnet import Subnet
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.models.task import Task
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import check_called_with
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import (
    OPEN_URL_FUNC, TATLIN_API_CLIENT_MODULE,
)


class TestSubnet:

    def test_create_subnet(
        self,
        tatlin,
        make_mock,
        open_url_kwargs,
        subnets_data,
    ):
        # Mock uuid4
        make_mock(TATLIN_API_CLIENT_MODULE + '.uuid4', return_value='1')

        # Mock open_url with task data
        open_url_mock = make_mock(
            OPEN_URL_FUNC,
            return_value={'id': 1},
        )

        # Create subnet
        task = tatlin.create_subnet(
            name='subnet1',
            ip_start='1.1.1.1',
            ip_end='2.2.2.2',
        )

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}/create'.format(
                eps.DASHBOARD_SUBNETS_ENDPOINT),
            headers={'Content-Type': 'application/json'},
            data={
                'id': '1',
                'name': 'subnet1',
                'ips': ['1.1.1.1', '2.2.2.2'],
            },
        )

        # Result: Request with expected params was sent
        check_called_with(open_url_mock, **open_url_kwargs)

        # Result: Tatlin`s Task was returned
        assert isinstance(task, Task)
        assert task.id == 1

    def test_get_subnets(self, tatlin, make_mock, subnets_data):

        # Mock open_url with subnets data
        make_mock(
            OPEN_URL_FUNC,
            return_value=subnets_data,
        )

        # Get subnets
        subnets = tatlin.get_subnets()

        # Result: Subnets with expected params were returned
        assert len(subnets) == 2

        assert subnets[0].name == 'subnet1'
        assert subnets[0].ip_start == '1.1.1.1'
        assert subnets[0].ip_end == '2.2.2.2'

        assert subnets[1].name == 'subnet2'
        assert subnets[1].ip_start == '8.8.8.8'
        assert subnets[1].ip_end == '9.9.9.9'

    def test_get_subnet(self, tatlin, make_mock, subnets_data):

        # Mock open_url with subnets data
        make_mock(
            OPEN_URL_FUNC,
            return_value=subnets_data,
        )

        # Get subnet
        subnet = tatlin.get_subnet('subnet2')

        # Result: Subnet with expected params was returned
        assert subnet.name == 'subnet2'
        assert subnet.ip_start == '8.8.8.8'
        assert subnet.ip_end == '9.9.9.9'

    @pytest.mark.parametrize(
        'ips_for_update, ips_expected', [
            [{'ip_start': '3.3.3.3', 'ip_end': '4.4.4.4'},
             ['3.3.3.3', '4.4.4.4']],
            [{'ip_start': None, 'ip_end': '4.4.4.4'},
             ['1.1.1.1', '4.4.4.4']],
            [{'ip_start': '1.1.1.2', 'ip_end': None},
             ['1.1.1.2', '1.1.1.100']]
        ]
    )
    def test_update_subnet(
        self,
        tatlin,
        make_mock,
        open_url_kwargs,
        ips_for_update,
        ips_expected,
    ):
        # Create Subnet Object
        subnet = Subnet(client=tatlin, **dict(
            id='11',
            name='subnet1',
            ips=['1.1.1.1', '1.1.1.100']
        ))

        # Mock open_url with task data
        open_url_mock = make_mock(
            OPEN_URL_FUNC,
            return_value={'id': 1},
        )

        # Update subnet
        task = subnet.update(
            ip_start=ips_for_update['ip_start'],
            ip_end=ips_for_update['ip_end'],
        )

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{ep}/update/{id}'.format(
                ep=eps.DASHBOARD_SUBNETS_ENDPOINT,
                id='11',
            ),
            headers={'Content-Type': 'application/json'},
            data={
                'name': 'subnet1',
                'ips': ips_expected,
            },
        )

        # Result: Request with expected params was sent
        check_called_with(open_url_mock, **open_url_kwargs)

        # Result: Tatlin`s Task was returned
        assert isinstance(task, Task)
        assert task.id == 1

    def test_subnet_remove(self, tatlin, make_mock, open_url_kwargs):
        # Create Subnet Object
        subnet = Subnet(client=tatlin, **dict(
            id='11',
            name='subnet1',
            ips=['1.1.1.1', '1.1.1.100']
        ))

        # Mock open_url with task data
        open_url_mock = make_mock(
            OPEN_URL_FUNC,
            return_value={'id': 1},
        )

        # Remove subnet
        task = subnet.remove()

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{ep}/delete/{id}'.format(
                ep=eps.DASHBOARD_SUBNETS_ENDPOINT,
                id='11',
            ),
        )

        # Result: Request with expected params was sent
        check_called_with(open_url_mock, **open_url_kwargs)

        # Result: Tatlin`s Task was returned
        assert isinstance(task, Task)
        assert task.id == 1
