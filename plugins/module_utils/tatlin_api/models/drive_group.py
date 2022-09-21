# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints as eps
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.utils import to_bytes
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.models.drive import Drive
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.models.pool import Pool, PROVISION_TYPE
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError

try:
    from typing import List, Dict, Optional, Union
except ImportError:
    List = Dict = Optional = Union = None


class DRIVE_GROUP_STATUS:
    WARNING = 'Warning'
    ERROR = 'Error'
    READY = 'Ready'


class DriveGroup:

    def __init__(self, client, **drive_group_data):
        self._client = client
        self._data = drive_group_data

        self.drives = []
        self.load_drives()

    @property
    def capacity_available(self):  # type: () -> int
        rv = int(self._data['availableCapacity']) \
            if self._data.get('availableCapacity') is not None else None
        return rv

    @property
    def capacity_failed(self):  # type: () -> int
        rv = int(self._data['failedCapacity']) \
            if self._data.get('failedCapacity') is not None else None
        return rv

    @property
    def capacity_total(self):  # type: () -> int
        rv = int(self._data['totalCapacity']) \
            if self._data.get('totalCapacity') is not None else None
        return rv

    @property
    def capacity_used(self):  # type: () -> int
        rv = int(self._data['usedCapacity']) \
            if self._data.get('usedCapacity') is not None else None
        return rv

    @property
    def cold_archive(self):  # type: () -> bool
        return self._data.get('coldArchive')

    @property
    def drive_capacity(self):  # type: () -> int
        rv = int(self._data['diskCapacity']) \
            if self._data.get('diskCapacity') is not None else None
        return rv

    @property
    def drives_failed(self):  # type: () -> int
        return self._data.get('failedDisks')

    @property
    def drives_available(self):  # type: () -> int
        return self._data.get('availableDisks')

    @property
    def drives_total(self):  # type: () -> int
        return self._data.get('totalDisks')

    @property
    def drives_used(self):  # type: () -> int
        return self._data.get('usedDisks')

    @property
    def drives_warning(self):  # type: () -> int
        return self._data.get('warningDisks')

    @property
    def model(self):  # type: () -> str
        return self._data.get('model')

    @property
    def id(self):  # type: () -> str
        rv = self._data.get('id')
        if rv is None:
            raise AttributeError(
                'DriveGroup object has no id value'
            )
        return rv

    @property
    def name(self):  # type: () -> str
        return self._data.get('name')

    @property
    def status(self):  # type: () -> str
        if self.drives_failed > 0:
            return DRIVE_GROUP_STATUS.ERROR
        if self.drives_warning > 0:
            return DRIVE_GROUP_STATUS.WARNING
        return DRIVE_GROUP_STATUS.READY

    @property
    def type(self):  # type: () -> str
        return self._data.get('diskType')

    def create_pool(
        self,
        name,  # type: str
        protection,  # type: str
        provision,  # type: str
        size=None,  # type: Union[str, int]
        drives_count=None,  # type: int
        spare_count=None,  # type: int
        stripe_size=None,  # type: Union[str, int]
        warning_threshold=None,  # type: int
        critical_threshold=None,  # type: int
    ):
        self._check_pool_capacity(pool_size=size, drives_count=drives_count)

        allowed_provisions = (PROVISION_TYPE.THIN, PROVISION_TYPE.THICK)
        if provision not in allowed_provisions:
            raise TatlinClientError(
                'Wrong provision type: {0}. Only {1} are allowed'.format(
                    provision, ', '.join(allowed_provisions))
            )

        if size and isinstance(size, str):
            size = to_bytes(size)

        if stripe_size and isinstance(stripe_size, str):
            stripe_size = to_bytes(stripe_size)

        req_body = {
            'name': name,
            'media': {
                'name': self.name,
                'model': self.model,
                'coldArchive': self.cold_archive,
            },
            'disks': str(drives_count) if drives_count else None,
            'capacity': str(size) if size else None,
            'protection': protection,
            'spare': str(spare_count) if spare_count is not None else '',
            'stripe_size': stripe_size,
            'thinProvision': provision == PROVISION_TYPE.THIN,
            'soft_alert_threshold': warning_threshold,
            'critical_alert_threshold': critical_threshold,
        }

        pool_data = self._client.post(
            path=eps.HEALTH_POOLS_ENDPOINT,
            body=req_body,
        ).json

        new_pool = Pool(client=self._client, drive_group=self, **pool_data)
        return new_pool

    def get_drive(self, drive_id):  # type: (str) -> Optional[Drive]
        return next((d for d in self.drives if d.id == drive_id), None)

    def get_pool(self, name):  # type: (str) -> Optional[Pool]
        return next((p for p in self.get_pools() if p.name == name), None)

    def get_pools(self):  # type: () -> List[Pool]
        rv = []

        pools_data = self._client.get(eps.HEALTH_POOLS_ENDPOINT).json
        for pool_data in pools_data:
            pool_drive_group = pool_data['media']['model']
            if self.id == pool_drive_group:
                new_pool = Pool(
                    client=self._client,
                    drive_group=self,
                    **pool_data
                )

                rv.append(new_pool)

        return rv

    def get_real_pool_size(
        self,
        protection,  # type: str
        size=None,  # type: Union[int, str]
        drives_count=None,  # type: int
        spare_count=None,  # type: int
    ):  # type: (...) -> int

        if not size and not drives_count:
            raise TatlinClientError(
                'size or drives_count arguments must be defined')

        if size and drives_count:
            raise TatlinClientError(
                'Only one of the arguments size and '
                'drives_count must be defined'
            )

        protection = protection.replace('+', '%2B')
        model = self.model.replace('+', '%2B')

        path = '{ep}/realSize?protection={protection}&media={media}'.format(
            ep=eps.HEALTH_POOLS_ENDPOINT,
            protection=protection,
            media=model,
        )

        if size:
            if isinstance(size, str):
                size = to_bytes(size)
            path += '&capacity={0}'.format(size)

        if drives_count:
            path += '&disks={0}'.format(drives_count)

        if spare_count:
            path += '&spare={0}'.format(spare_count)

        real_size = self._client.get(path).json

        return real_size

    def load(self):  # type: () -> None
        all_groups_data = self._client.get(eps.HEALTH_MEDIAS_ENDPOINT).json
        for group_data in all_groups_data.values():
            if group_data['id'] == self.id:
                self._data = group_data
                break

        self.load_drives()

    def load_drives(self):
        self.drives = []
        pools = self.get_pools()

        for drive_data in self._data.get('disks', []):
            drive_pool = next((
                pool for pool in pools
                if drive_data['id'] in pool.get_drive_ids()
            ), None)

            self.drives.append(Drive(
                client=self._client, drive_group=self, pool=drive_pool, **drive_data))

    @staticmethod
    def _check_pool_capacity(pool_size, drives_count):
        if pool_size is None and drives_count is None:
            raise TatlinClientError(
                'One of the following arguments is '
                'required: pool_size, drives_count'
            )

        if pool_size is not None and drives_count is not None:
            raise TatlinClientError(
                'pool_size and drives_count arguments were '
                'defined. Only one of them is required'
            )
