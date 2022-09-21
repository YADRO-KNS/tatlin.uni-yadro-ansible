# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.models.pool import Pool
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.models.drive import Drive
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import HEALTH_POOLS_ENDPOINT
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.utils import check_called_with
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import (
    POOL_CLASS, OPEN_URL_FUNC, DRIVE_GROUP_CLASS)


class TestPool:

    def test_load(
        self, tatlin, make_mock, drives_groups_data, pools_data
    ):
        # Make mocks for drive group creation
        make_mock(
            OPEN_URL_FUNC,
            return_value=[drives_groups_data, {}],
            chain_calls=True,
        )

        # Get drive group
        drive_group = tatlin.get_drive_groups()[0]

        # Create pool object
        pool = Pool(
            client=tatlin,
            drive_group=drive_group,
            id='pool_id',
        )

        # Check pool drives are empty
        assert len(pool.drives) == 0

        # Mock open_url response with pools data
        pools_data = pools_data[0]
        pools_data['thinProvision'] = True
        pools_data['soft_alert_threshold'] = 70
        pools_data['critical_alert_threshold'] = 90
        make_mock(OPEN_URL_FUNC, return_value=pools_data)

        # Load pool
        pool.load()

        make_mock(
            DRIVE_GROUP_CLASS + '.get_pools',
            return_value=[pool],
        )

        # Result: Pool has expected parameters
        assert pool is not None
        assert pool.id == '28118216-74eb-4ba2-8e01-be894b878de1'
        assert pool.name == 'testpool'
        assert pool.status == 'ready'
        assert pool.provision == 'thin'
        assert pool.protection == '2+1'
        assert pool.capacity_used == 369098752
        assert pool.capacity_available == 33554432
        assert pool.capacity_failed == 0
        assert pool.capacity_total == 402653184
        assert pool.stripe_size == 8192
        assert pool.spare_count == 1
        assert pool.warning_threshold == 70
        assert pool.critical_threshold == 90
        assert len(pool.drives) > 0
        assert isinstance(pool.drives[0], Drive)

    def test_get_resources(self, tatlin, make_mock, resources_data):
        # Create pool object
        pool = Pool(
            client=tatlin,
            drive_group=None,
            id=resources_data[0]['poolId'],
        )

        # Mock open_url with resources data
        make_mock(OPEN_URL_FUNC, return_value=resources_data)

        # Get pool resources
        resources = pool.get_resources()

        # Result: Resources list is not empty
        assert len(resources) > 0

    def test_remove(self, tatlin, make_mock, open_url_kwargs, pools_data):
        # Create pool object
        pool = Pool(client=tatlin, drive_group=None, **pools_data[0])

        # Mock open_url without data
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Remove pool
        pool.remove()

        # Defining expected call parameters
        open_url_kwargs.update(
            method='DELETE',
            url='https://localhost/{0}/{1}'.format(
                HEALTH_POOLS_ENDPOINT, pool.id),
        )

        # Result: open_url was called with expected params
        check_called_with(open_url_mock, **open_url_kwargs)

    def test_remove_fail(self, tatlin, make_mock, resources_data):
        # Mock load_resources
        make_mock(OPEN_URL_FUNC, return_value=resources_data)

        # Create pool object
        pool = Pool(
            client=tatlin,
            drive_group=None,
            id=resources_data[0]['poolId'],
        )

        # Mock open_url with resources data
        make_mock(OPEN_URL_FUNC, return_value=resources_data)

        # Remove pool
        # Result: Error was raised
        with pytest.raises(TatlinClientError):
            pool.remove()

    def test_is_ready(self, tatlin, make_mock):
        # Create pool object with ready status
        pool = Pool(
            client=tatlin,
            drive_group=None,
            status='ready',
            id='pool_id',
        )

        # Result: is_ready method return True
        assert pool.is_ready()

        # Set pool status error
        pool._data['status'] = 'error'

        # Result: is_ready method return False
        assert not pool.is_ready()

    def test_set_drives_count(
        self,
        tatlin,
        make_mock,
        open_url_kwargs,
        drives_groups_data,
        pools_data,
    ):
        # Make mocks for drive group creation
        make_mock(POOL_CLASS + '.load')
        make_mock(
            OPEN_URL_FUNC,
            return_value=[drives_groups_data, pools_data, pools_data],
            chain_calls=True,
        )

        # Get drive group
        drive_group = tatlin.get_drive_groups()[0]

        # Create pool object
        pool = drive_group.get_pool(pools_data[0]['name'])

        # Mock open_url without data
        open_url_mock = make_mock(OPEN_URL_FUNC)

        # Set pool drives count
        pool.set_drives_count(4)

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}/{1}/resize'.format(
                HEALTH_POOLS_ENDPOINT, pool.id),
            headers={'Content-Type': 'application/json'},
            data={'disks': 4},
        )

        check_called_with(open_url_mock, **open_url_kwargs)

    def test_set_drives_count_fail(
        self,
        tatlin,
        make_mock,
        open_url_kwargs,
        drives_groups_data,
        pools_data,
    ):
        # Make mocks for drive group creation
        make_mock(POOL_CLASS + '.load')
        make_mock(
            OPEN_URL_FUNC,
            return_value=[drives_groups_data, pools_data, pools_data],
            chain_calls=True,
        )

        # Get drive group
        drive_group = tatlin.get_drive_groups()[0]

        # Create pool object
        pool = drive_group.get_pool(pools_data[0]['name'])

        # Mock open_url without data
        make_mock(OPEN_URL_FUNC)

        # Set pool drives count
        # Result: Error was raised
        with pytest.raises(TatlinClientError):
            pool.set_drives_count(1)

    def test_set_size(self, tatlin, make_mock, open_url_kwargs):
        # Mock load method
        make_mock(POOL_CLASS + '.load')

        # Create pool object with capacity
        pool = Pool(
            client=tatlin,
            drive_group=None,
            capacity=201326592,
            id='pool_id',
        )

        # Mock open_url without data
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Set new pool size
        pool.set_size('288MiB')

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}/{1}/resize'.format(
                HEALTH_POOLS_ENDPOINT, pool.id),
            headers={'Content-Type': 'application/json'},
            data={'bytes': '301989888'}
        )

        # Result: open_url was called with expected params
        check_called_with(open_url_mock, **open_url_kwargs)

    def test_set_size_fail(self, tatlin, make_mock):
        # Mock load method
        make_mock(POOL_CLASS + '.load')

        # Create pool object with capacity
        pool = Pool(
            client=tatlin,
            drive_group=None,
            capacity=201326592,
            id='pool_id',
        )

        # Mock open_url without data
        make_mock(target=OPEN_URL_FUNC)

        # Set new pool size
        # Result: Error was raised
        with pytest.raises(TatlinClientError):
            pool.set_size('191MiB')

    def test_set_spare_count(self, tatlin, make_mock, open_url_kwargs):
        # Mock load method
        make_mock(POOL_CLASS + '.load')

        # Create pool object
        pool = Pool(client=tatlin, drive_group=None, id='pool_id')

        # Mock open_url without data
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Set new spare count
        pool.set_spare_count(10)

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}/{1}'.format(
                HEALTH_POOLS_ENDPOINT, pool.id),
            headers={'Content-Type': 'application/json'},
            data={'spare': '10'}
        )

        # Result: open_url was called with expected params
        check_called_with(open_url_mock, **open_url_kwargs)

    def test_set_thresholds(self, tatlin, make_mock, open_url_kwargs):
        # Mock load method
        make_mock(POOL_CLASS + '.load')

        # Create pool object with thin provision
        pool = Pool(
            client=tatlin,
            drive_group=None,
            thinProvision=True,
            id='pool_id',
        )

        # Mock open_url without data
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        # Set new thresholds
        pool.set_thresholds(warning_threshold=55, critical_threshold=87)

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}/{1}/alerts'.format(
                HEALTH_POOLS_ENDPOINT, pool.id),
            headers={'Content-Type': 'application/json'},
            data={
                'soft_alert_threshold': 55,
                'critical_alert_threshold': 87,
            }
        )

        # Result: open_url was called with expected params
        check_called_with(open_url_mock, **open_url_kwargs)

    def test_set_thresholds_fail_no_args(self, tatlin, make_mock):
        # Mock load method
        make_mock(POOL_CLASS + '.load')

        # Create pool object thin provision
        pool = Pool(
            client=tatlin,
            drive_group=None,
            thinProvision=True,
            id='pool_id'
        )

        # Mock open_url without data
        make_mock(target=OPEN_URL_FUNC)

        # Call method without arguments
        # Result: TypeError was raised
        with pytest.raises(TypeError):
            pool.set_thresholds()

    def test_set_thresholds_fail_provision(self, tatlin, make_mock):
        # Mock load method
        make_mock(POOL_CLASS + '.load')

        # Create pool object with thick provision
        pool = Pool(
            client=tatlin,
            drive_group=None,
            thinProvision=False,
            id='pool_id',
        )

        # Mock open_url without data
        make_mock(target=OPEN_URL_FUNC)

        # Set new thresholds
        # Result: Error was raised
        with pytest.raises(TatlinClientError):
            pool.set_thresholds(warning_threshold=55, critical_threshold=87)
