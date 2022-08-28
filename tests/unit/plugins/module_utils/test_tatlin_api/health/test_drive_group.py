# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import pytest
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import HEALTH_POOLS_ENDPOINT
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import OPEN_URL_FUNC
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import POOL_CLASS
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import (
    check_obj, check_called_with)


class TestDrives:

    def test_get_drive_group(
        self, tatlin, make_mock, drives_groups_data, pools_data
    ):
        # Make mocks for drive group creation
        make_mock(POOL_CLASS + '.load_resources')
        make_mock(
            target=OPEN_URL_FUNC,
            return_value=[drives_groups_data, pools_data],
            chain_calls=True,
        )

        # Get drive group
        drive_group = tatlin.get_drive_groups()[0]

        # Result: Drive group with expected params was returned
        assert drive_group.name == 'HDD_209.71MB'
        assert drive_group.type == 'HDD'
        assert drive_group.capacity_total == 8388608000
        assert drive_group.capacity_available == 7549747200
        assert drive_group.capacity_used == 838860800
        assert drive_group.capacity_failed == 0
        assert drive_group.drive_capacity == 209715200
        assert drive_group.drives_total == 40
        assert drive_group.drives_used == 4
        assert drive_group.drives_available == 36
        assert drive_group.drives_failed == 0
        assert drive_group.drives_warning == 0
        assert drive_group.status == 'Ready'

        # Result: Group contains drive with expected params
        drive = drive_group.drives[0]
        check_obj(drive, exp_params={
            'id': 'scsi-0YADRO_shared_disk_0450513bb2bbd68fdc7cb9f2e38d00c0',
            'model': 'YADRO-shared_disk-2.5+',
            'serial_number': '0450513bb2bbd68fdc7cb9f2e38d00c0',
            'size': 209715200,
            'slot': '4',
        })

        assert drive.bay == '1000000001', 'Drive has wrong bay'
        assert drive.status == 'Healthy', 'Drive has wrong status'

        # Result: Drive has pool with expected params
        pool = drive.pool
        assert pool is not None
        assert pool.id == '28118216-74eb-4ba2-8e01-be894b878de1'
        assert pool.name == 'testpool'
        assert pool.status == 'ready'
        assert pool.provision == 'thick'
        assert pool.protection == '2+1'
        assert pool.capacity_used == 369098752
        assert pool.capacity_available == 33554432
        assert pool.capacity_failed == 0
        assert pool.capacity_total == 402653184
        assert pool.stripe_size == 8192
        assert pool.drives == [drive]
        assert pool.spare_count == 1
        assert pool.warning_threshold is None
        assert pool.critical_threshold is None

    def test_warning_status(
        self, tatlin, make_mock, drives_groups_data, pools_data
    ):
        # Make mocks for drive group creation
        drives_groups_data['HDD_209715200']['warningDisks'] = 1
        drives_groups_data['HDD_209715200']['disks'][0]['state'] = 'warning'
        make_mock(POOL_CLASS + '.load_resources')
        make_mock(
            OPEN_URL_FUNC,
            return_value=[drives_groups_data, pools_data],
            chain_calls=True,
        )

        # Get drive group
        drive_group = tatlin.get_drive_groups()[0]

        # Result: Drive group has status Warning
        assert drive_group.status == 'Warning', 'Drive group has wrong status'
        assert drive_group.drives[0].status == 'Warning', 'Drive has wrong status'

    def test_error_status(
        self, tatlin, make_mock, drives_groups_data, pools_data
    ):
        # Make mocks for drive group creation
        drives_groups_data['HDD_209715200']['failedDisks'] = 1
        drives_groups_data['HDD_209715200']['disks'][0]['state'] = 'error'
        make_mock(POOL_CLASS + '.load_resources')
        make_mock(
            OPEN_URL_FUNC,
            return_value=[drives_groups_data, pools_data],
            chain_calls=True,
        )

        # Get drive group
        drive_group = tatlin.get_drive_groups()[0]

        # Result: Drive group has status Warning
        assert drive_group.status == 'Error', 'Drive group has wrong status'
        assert drive_group.drives[0].status == 'Error', 'Drive has wrong status'

    @pytest.mark.parametrize(
        'provision, warning_threshold, critical_threshold, thin_provision',
        [['thin', 50, 85, True], ['thick', None, None, False]]
    )
    def test_create_pool(
        self,
        tatlin,
        make_mock,
        open_url_kwargs,
        drives_groups_data,
        provision,
        warning_threshold,
        critical_threshold,
        thin_provision,
    ):
        # Make mocks for drive group creation
        make_mock(POOL_CLASS + '.load_resources')
        make_mock(
            OPEN_URL_FUNC,
            return_value=[drives_groups_data, {}],
            chain_calls=True,
        )

        # Get drive group
        drive_group = tatlin.get_drive_groups()[0]

        # Mock open_url without data
        open_url_mock = make_mock(OPEN_URL_FUNC)

        # Mock Pool.load_resources()
        make_mock(POOL_CLASS + '.load_resources')

        # Create pool
        drive_group.create_pool(
            name='newpool',
            protection='1+1',
            provision=provision,
            drives_count=3,
            spare_count=1,
            stripe_size=8192,
            warning_threshold=warning_threshold,
            critical_threshold=critical_threshold,
        )

        # Defining expected call parameters
        open_url_kwargs.update(
            method='POST',
            url='https://localhost/{0}'.format(HEALTH_POOLS_ENDPOINT),
            headers={'Content-Type': 'application/json'},
            data={
                'name': 'newpool',
                'media': {
                    'name': drive_group.name,
                    'model': drive_group.model,
                    'coldArchive': drive_group.cold_archive,
                },
                'disks': '3',
                'capacity': None,
                'protection': '1+1',
                'spare': '1',
                'stripe_size': 8192,
                'thinProvision': thin_provision,
                'soft_alert_threshold': warning_threshold,
                'critical_alert_threshold': critical_threshold,
            },
        )

        # Result: open_url was called with expected params
        check_called_with(open_url_mock, **open_url_kwargs)

    def test_create_pool_format_sizes(
        self, tatlin, make_mock, open_url_kwargs, drives_groups_data
    ):
        # Make mocks for drive group creation
        make_mock(POOL_CLASS + '.load_resources')
        make_mock(
            OPEN_URL_FUNC,
            return_value=[drives_groups_data, {}],
            chain_calls=True,
        )

        # Get drive group
        drive_group = tatlin.get_drive_groups()[0]

        # Mock open_url without data
        open_url_mock = make_mock(OPEN_URL_FUNC)

        # Mock Pool.load_resources()
        make_mock(POOL_CLASS + '.load_resources')

        # Create pool
        drive_group.create_pool(
            name='newpool',
            protection='1+1',
            provision='thick',
            size='192 MiB',
            spare_count=1,
            stripe_size='4 KiB',
        )

        # Defining expected call parameters
        open_url_kwargs.update(
            method='POST',
            url='https://localhost/{0}'.format(HEALTH_POOLS_ENDPOINT),
            headers={'Content-Type': 'application/json'},
            data={
                'name': 'newpool',
                'media': {
                    'name': drive_group.name,
                    'model': drive_group.model,
                    'coldArchive': drive_group.cold_archive,
                },
                'disks': None,
                'capacity': '201326592',
                'protection': '1+1',
                'spare': '1',
                'stripe_size': 4096,
                'thinProvision': False,
                'soft_alert_threshold': None,
                'critical_alert_threshold': None,
            },
        )

        # Result: open_url was called with expected params
        check_called_with(open_url_mock, **open_url_kwargs)

    def test_create_pool_wrong_provision(
        self, tatlin, make_mock, drives_groups_data
    ):
        # Make mocks for drive group creation
        make_mock(POOL_CLASS + '.load_resources')
        make_mock(
            OPEN_URL_FUNC,
            return_value=[drives_groups_data, {}],
            chain_calls=True
        )

        # Get drive group
        drive_group = tatlin.get_drive_groups()[0]

        # Create pool
        # Result: Exception is raised
        with pytest.raises(TatlinClientError):
            drive_group.create_pool(
                name='newpool',
                protection='1+1',
                provision='test',
                size='192 MiB',
                spare_count=1,
                stripe_size='4 KiB',
            )

    def test_get_real_pool_size(
        self, tatlin, make_mock, open_url_kwargs, drives_groups_data
    ):
        # Make mocks for drive group creation
        make_mock(POOL_CLASS + '.load_resources')
        make_mock(
            OPEN_URL_FUNC,
            return_value=[drives_groups_data, {}],
            chain_calls=True,
        )

        # Get drive group
        drive_group = tatlin.get_drive_groups()[0]

        # Mock open_url without data
        open_url_mock = make_mock(OPEN_URL_FUNC)

        drive_group.get_real_pool_size(
            protection='1+1',
            size='192 MiB',
            spare_count=2,
        )

        # Defining expected call parameters
        open_url_kwargs.update(
            method='GET',
            url='https://localhost/{ep}/realSize?protection={protection}&'
            'media={media}&capacity={capacity}&spare={spare}'.format(
                ep=HEALTH_POOLS_ENDPOINT,
                protection='1%2B1',
                media=drive_group.model,
                capacity=201326592,
                spare=2,
            ),
        )

        check_called_with(open_url_mock, **open_url_kwargs)

    def test_load_pools(
        self, tatlin, make_mock, drives_groups_data, pools_data
    ):
        # Make mocks for drive group creation
        make_mock(POOL_CLASS + '.load_resources')
        make_mock(
            OPEN_URL_FUNC,
            return_value=[drives_groups_data, {}],
            chain_calls=True,
        )

        # Get drive group
        drive_group = tatlin.get_drive_groups()[0]

        # Ensure that drive group has no pools
        assert len(drive_group.pools) == 0

        # Mock open_url response with pools data
        make_mock(OPEN_URL_FUNC, return_value=pools_data)
        make_mock(POOL_CLASS + '.load_resources')

        # Load pools
        drive_group.load_pools()

        # Result: Drive group pools are not empty
        assert len(drive_group.pools) > 0
