#!/usr/bin/python
# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r"""
---
module: tatlin_sp_pool
short_description: Create, modify or destroy a pool
version_added: "1.0.0"
description:
  - This module is intended to create new pool and
    change or remove existing pool
  - Supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin.connection_options
options:
  drive_group:
    required: True
    type: str
    description: Name of the drive group
  name:
    required: True
    type: str
    description: Name of the pool
  protection:
    required: False
    type: str
    choices: [
      '1+1', '2+1', '2+2', '4+1', '4+2', '4+3', '4+4', '8+1',
      '8+2', '8+3', '8+4', '8+5', '8+6', '8+7', '8+8'
      ]
    description:
      - Data protection scheme
      - Required when new pool is creating
  provision:
    required: False
    type: str
    choices: ['thin', 'thick']
    description:
      - Type of resources reservation
      - Required if new pool is creating
  size:
    required: False
    type: str
    description:
      - Pool volume
      - One of the following arguments is required, when
        new pool is creating - C(size), C(device_count)
      - Mutually exclusive with C(device_count)
      - Can be presented as a string number with postfix.
        For example '100 MiB'. Following postfixes are allowed -
        [B, KB, MB, GB, TB, PB, EB, ZB, YB, KiB, MiB, GiB, TiB, PiB, EiB, ZiB, YiB]
      - If no postfix is passed, 'B' (bytes) will be used.
  drives_count:
    required: False
    type: int
    description:
      - Pool size in disks
      - One of the following arguments is required, when
        new pool is creating - C(size), C(device_count)
      - Mutually exclusive with C(size)
  spare_count:
    required: False
    type: int
    description: Count of reserved drives
  stripe_size:
    required: False
    type: str
    description: Size of stripe
  warning_threshold:
    required: False
    type: int
    description:
      - Pool usage threshold in % (from 1 to 99) for sending alerts
        with level Warning.
      - Used only with I(provision) == C(thin)
  critical_threshold:
    required: False
    type: int
    description:
      - Pool usage threshold in % (from 1 to 99) for sending alerts
        with level Critical.
      - Used only with I(provision) == C(thick)
  state:
    type: str
    choices: [present, absent]
    default: present
    description:
      - C(present) create new pool or change existing
      - With existing pool it is allowed only resizing
        (I(size) or I(drives_count)) and changing I(spare_count)
        and thresholds
      - C(absent) removes existing pool. Only pool without
        resources can be removed
  wait_timeout:
    type: int
    required: False
    default: 60
    description: The number of seconds for waiting until pool will be ready
notes:
  - Fact pool size may differ from C(size) value. Real size will be returned
    by module
  - Pool removing takes some time in Tatlin. It means that after execution
    module with state C(absent) task completes, but pool can still exist.
    Therefore, if new pool is created after removing pool with same name,
    it needs to be ensure that pool doesn't exists. This operation is out of
    scope of this module. M(yadro.tatlin.tatlin_sp_pools_info) can be used in
    that case
"""

RETURN = r"""
---
msg:
  type: str
  returned: always
  description: Operation status message
error:
  type: str
  returned: on error
  description: Error details if raised
real_size:
  type: str
  returned: on success
  description:
    - Real pool size (may be defferent from I(size))
    - Always None if I(state) is C(absent)
"""

EXAMPLES = r"""
---
- name: Create new pool
  yadro.tatlin.tatlin_sp_pool:
    connection: "{{ connection }}"
    drive_group: HDD_209.71MB
    name: testpool
    protection: '1+1'
    provision: 'thin'
    size: 192 MiB
    spare_count: 1
    stripe_size: 4KiB
    warning_threshold: 80
    critical_threshold: 95

- name: Resize pool
  yadro.tatlin.tatlin_sp_pool:
    connection: "{{ connection }}"
    drive_group: HDD_209.71MB
    name: testpool
    drives_count: 5

- name: Update thresholds
  yadro.tatlin.tatlin_sp_pool:
    connection: "{{ connection }}"
    drive_group: HDD_209.71MB
    name: testpool
    warning_threshold: 75
    critical_threshold: 90

- name: Remove pool
  yadro.tatlin.tatlin_sp_pool:
    connection: "{{ connection }}"
    drive_group: HDD_209.71MB
    name: testpool
    state: absent
"""


import time
from functools import partial
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_module import TatlinModule
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.utils import to_bytes


class TatlinPoolModule(TatlinModule):

    def __init__(self):
        protection_choices = (
            '1+1', '2+1', '2+2', '4+1', '4+2', '4+3', '4+4', '8+1',
            '8+2', '8+3', '8+4', '8+5', '8+6', '8+7', '8+8',
        )

        argument_spec = {
            'drive_group': {'type': 'str', 'required': True},
            'name': {'type': 'str', 'required': True},
            'protection': {
                'type': 'str',
                'choices': protection_choices,
                'required': False,
            },
            'provision': {
                'type': 'str',
                'choices': ['thin', 'thick'],
                'required': False,
            },
            'size': {'type': 'str', 'required': False},
            'drives_count': {'type': 'int', 'required': False},
            'spare_count': {'type': 'int', 'required': False},
            'stripe_size': {'type': 'str', 'required': False},
            'warning_threshold': {'type': 'int', 'required': False},
            'critical_threshold': {'type': 'int', 'required': False},
            'state': {
                'type': 'str',
                'required': False,
                'default': 'present',
                'choices': ['present', 'absent'],
            },
            'wait_timeout': {'type': 'int', 'required': False, 'default': 60},
        }

        super(TatlinPoolModule, self).__init__(
            argument_spec=argument_spec,
            supports_check_mode=True,
            mutually_exclusive=[('size', 'drives_count')],
        )

    def run(self):
        if self.params['provision'] == 'thick' and any([
            self.params['warning_threshold'] is not None,
            self.params['critical_threshold'] is not None,
        ]):
            self.fail_json(
                changed=False,
                error='Mutually exclusive parameters',
                msg='Provision thick is mutually exclusive with '
                    'warning_threshold, critical_threshold',
            )

        actions = []
        real_size = None
        drive_group = self.tatlin.get_drive_group(self.params['drive_group'])
        if drive_group is None:
            self.fail_json(
                changed=False,
                error='Drive group not found',
                msg='Drive group {0} does not exist'.format(
                    self.params['drive_group']),
            )

        pool = drive_group.get_pool(self.params['name'])

        if self.params['state'] == 'present':
            if pool is None:
                self.validate_params_create()
                actions.append(partial(
                    drive_group.create_pool,
                    name=self.params['name'],
                    protection=self.params['protection'],
                    provision=self.params['provision'],
                    size=self.params['size'],
                    drives_count=self.params['drives_count'],
                    spare_count=self.params['spare_count'],
                    stripe_size=self.params['stripe_size'],
                    warning_threshold=self.params['warning_threshold'],
                    critical_threshold=self.params['critical_threshold'],
                ))
            else:
                self.validate_params_change(pool)

                new_spare_count = self.params['spare_count']
                if all([
                    new_spare_count is not None,
                    new_spare_count != pool.spare_count,
                ]):
                    actions.append(partial(
                        pool.set_spare_count,
                        spare_count=new_spare_count
                    ))

                new_drives_count = self.params['drives_count']
                if all([
                    new_drives_count is not None,
                    new_drives_count != len(pool.drives),
                ]):
                    actions.append(partial(
                        pool.set_drives_count,
                        drives_count=new_drives_count,
                    ))

                if self.params['size'] is not None:
                    real_pool_size = drive_group.get_real_pool_size(
                        protection=pool.protection,
                        size=self.params['size'],
                        spare_count=pool.spare_count,
                    )

                    if real_pool_size != pool.capacity_total:
                        actions.append(partial(
                            pool.set_size,
                            size=real_pool_size,
                        ))

                new_warn = self.params['warning_threshold']
                new_crit = self.params['critical_threshold']
                if any([
                    new_warn is not None and new_warn != pool.warning_threshold,
                    new_crit is not None and new_crit != pool.critical_threshold
                ]):
                    actions.append(partial(
                        pool.set_thresholds,
                        warning_threshold=new_warn,
                        critical_threshold=new_crit,
                    ))
        else:
            if pool is not None and len(pool.get_resources()) > 0:
                # state absent, can't remove
                self.fail_json(
                    changed=False,
                    error='Removing pool error',
                    msg='It is prohibited to remove '
                        'pool with existing resources',
                )
            elif pool is not None and not pool.is_deleting():
                # state absent, can remove pool
                actions.append(partial(pool.remove))

        if len(actions) == 0:
            if self.params['state'] == 'present':
                real_size = pool.capacity_total

            self.exit_json(
                msg='No changes required',
                changed=False,
                real_size=real_size,
            )

        if not self.check_mode:
            for action in actions:
                try:
                    action()
                    self.changed = True
                except Exception as e:
                    self.fail_json(
                        msg='Operation failed',
                        error='{0}: {1}'.format(type(e).__name__, e),
                        changed=self.changed,
                        real_size=None,
                    )

        real_size = self.get_output_real_size(drive_group, pool)

        self.exit_json(
            msg='Operation successful',
            changed=True,
            real_size=real_size,
        )

    def get_output_real_size(self, drive_group, pool):
        if self.params['state'] == 'absent':
            return None

        real_size = None
        if self.check_mode and pool is None:
            real_size = drive_group.get_real_pool_size(
                protection=self.params['protection'],
                size=self.params['size'],
                drives_count=self.params['drives_count'],
                spare_count=self.params['spare_count'],
            )
        elif self.check_mode and self.params['size']:
            real_size = drive_group.get_real_pool_size(
                protection=pool.protection,
                size=self.params['size'],
                spare_count=self.params['spare_count'] or pool.spare_count,
            )
        elif self.check_mode and self.params['drives_count']:
            real_size = drive_group.get_real_pool_size(
                protection=pool.protection,
                drives_count=self.params['drives_count'],
                spare_count=self.params['spare_count'] or pool.spare_count,
            )
        elif not self.check_mode:
            pool = drive_group.get_pool(self.params['name'])
            self.wait_pool_is_ready(pool)
            real_size = pool.capacity_total

        return real_size

    def validate_params_create(self):
        missing_params = []
        for param_name in ('protection', 'provision'):
            if self.params[param_name] is None:
                missing_params.append(param_name)

        if len(missing_params) > 0:
            self.fail_json(
                changed=False,
                error='Missing required arguments',
                msg='Missing required arguments: {0}'.format(
                    ', '.join(missing_params)),
            )

        if all([
            self.params['drives_count'] is None,
            self.params['size'] is None,
        ]):
            self.fail_json(
                changed=False,
                error='Missing required arguments',
                msg='One of following arguments is required: '
                    'drives_count, size',
            )

    def validate_params_change(self, pool):
        forbidden_params = (
            'protection',
            'provision',
            'stripe_size',
        )

        for param_name in forbidden_params:
            new_value = self.params[param_name]
            if new_value is None:
                continue

            if param_name == 'stripe_size':
                new_value = to_bytes(self.params['stripe_size'])

            old_value = getattr(pool, param_name)

            if new_value != old_value:
                msg = 'It is prohibited to change following parameters ' \
                      'for existing pool: {forbidden_params}. ' \
                      '{param_name} is changing. Old value: {old_value}. ' \
                      'New value: {new_value}'
                self.fail_json(
                    changed=False,
                    error='Changing forbidden parameters',
                    msg=msg.format(
                        forbidden_params=', '.join(forbidden_params),
                        param_name=param_name,
                        old_value=old_value,
                        new_value=new_value,
                    )
                )

    def wait_pool_is_ready(self, pool):
        pool.load()
        start_time = time.time()
        while not pool.is_ready() or pool.is_resizing():
            time.sleep(1)

            if time.time() - start_time > self.params['wait_timeout']:
                self.fail_json(
                    changed=False,
                    error='Timeout error',
                    msg='Changed pool has not become ready',
                )

            pool.load()


def main():
    TatlinPoolModule()


if __name__ == "__main__":
    main()
