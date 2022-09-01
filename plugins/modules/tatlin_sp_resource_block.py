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
module: tatlin_sp_resource_block
short_description: Create or modify a resource
version_added: "1.0.0"
description:
  - This module is intended to create new resource and
    change existing resource
  - Supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin.connection_options
options:
  name:
    required: True
    type: str
    description: Name of the resource
  pool:
    required: True
    type: str
    description: Name of the pool that includes the resource
  name_template:
    required: False
    type: str
    description:
      - Template for bulk mode creation.
      - Possible formats - '1-3', '1-3,4, 7-10', '0-99'
      - Example - with I(name_template='1-3') and I(name='res_') 3 resources
        with names 'res_1', 'res_2', 'res_3' will be created
  size:
    required: False
    type: str
    description:
      - Resource volume
      - Required if new resource is creating
      - Can be presented as a string number with postfix
        For example '100 MiB'. Following postfixes are allowed -
        [B, KB, MB, GB, TB, PB, EB, ZB, YB, KiB, MiB, GiB, TiB, PiB, EiB, ZiB, YiB]
      - If no postfix is passed, 'B' (bytes) will be used
  size_format:
    required: False
    type: str
    choices: ['512e', '4kn']
    default: '4kn'
    description: Sector size format
  read_cache:
    required: False
    type: bool
    default: True
    description: Cache reading
  write_cache:
    required: False
    type: bool
    default: True
    description: Cache writing
  warning_threshold:
    required: False
    type: int
    description: Warning alert threshold percentage
  ports:
    required: False
    type: list
    elements: str
    description: Names of the pools for export resources
  hosts:
    required: False
    type: list
    elements: str
    description: Names of the hosts for export resources
  host_groups:
    required: False
    type: list
    elements: str
    description: Names of the host groups for export resources
  wait:
    required: False
    type: bool
    default: True
    description:
      - Wait until resource or resources will be created
      - Irrelevant for bulk resources changing
  wait_timeout:
    required: False
    type: int
    default: 300
    description: Number of seconds to wait when I(wait=true)
notes:
  - Creating resources use bulk mode with asynchronous mode even for single
    resource. It is possible to wait until creating will be finished by using
    C(wait=True) or ignore waiting by using C(wait=False)
  - Changing resources in bulk mode is also possible but not in asynchronous
    mode. It means that at least one request will be send for changing each
    resource
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
created_resources:
  type: list
  elements: str
  returned: on success
  description: Names of the created resources
changed_resources:
  type: list
  elements: str
  returned: on success
  description: Names of the changed resources
"""

EXAMPLES = r"""
---
- name: Create one resource
  yadro.tatlin.tatlin_sp_resource_block:
    connection: "{{ connection }}"
    name: example_resource
    pool: example_pool
    size: 192MiB
    size_format: 512e
    read_cache: true
    write_cache: true
    warning_threshold: 90
    ports:
      - p00
      - p01
    hosts:
      - example_host1
      - example_host2
    host_groups:
      - example_host_group1
      - example_host_group2

- name: Create multiple resources
  yadro.tatlin.tatlin_sp_resource_block:
    connection: "{{ connection }}"
    name: example_resource
    name_template: 1-3,5,7-8
    pool: example_pool
    size: 192MiB
    size_format: 512e
    read_cache: true
    write_cache: true
    warning_threshold: 90
    ports:
      - p00
      - p01
    hosts:
      - example_host1
      - example_host2
    host_groups:
      - example_host_group1
      - example_host_group2

- name: Change one resource
  yadro.tatlin.tatlin_sp_resource_block:
    connection: "{{ connection }}"
    name: example_resource
    pool: example_pool
    size: 192MiB
    read_cache: False
    write_cache: False
    warning_threshold: 80
    ports:
      - p10
    hosts:
      - example_host2
      - example_host3
    host_groups:
      - example_host_group2
      - example_host_group3

- name: Change one resource
  yadro.tatlin.tatlin_sp_resource_block:
    connection: "{{ connection }}"
    name: example_resource
    name_template: 1-100
    pool: example_pool
    size: 192MiB
    read_cache: False
    write_cache: False
    warning_threshold: 80
    ports:
      - p10
    hosts:
      - example_host2
      - example_host3
    host_groups:
      - example_host_group2
      - example_host_group3
"""


import time
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_module import TatlinModule
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.utils import to_bytes


class TatlinResourceBlockModule(TatlinModule):

    def __init__(self):
        argument_spec = {
            'name': {'type': 'str', 'required': True},
            'pool': {'type': 'str', 'required': True},
            'name_template': {'type': 'str', 'required': False},
            'size': {'type': 'str', 'required': False},
            'size_format': {
                'type': 'str',
                'choices': ['512e', '4kn'],
                'default': '4kn',
                'required': False,
            },
            'read_cache': {
                'type': 'bool',
                'default': True,
                'required': False,
            },
            'write_cache': {
                'type': 'bool',
                'default': True,
                'required': False,
            },
            'warning_threshold': {'type': 'int', 'required': False},
            'ports': {'type': 'list', 'elements': 'str', 'required': False},
            'hosts': {'type': 'list', 'elements': 'str', 'required': False},
            'host_groups': {
                'type': 'list',
                'elements': 'str',
                'required': False,
            },
            'wait': {'type': 'bool', 'default': True, 'required': False},
            'wait_timeout': {'type': 'int', 'default': 300, 'required': False}
        }

        # Caching this objects, because there can be
        # too many identical queries with bulk update
        self._host_groups = None
        self._hosts = None
        self._ports = None

        super(TatlinResourceBlockModule, self).__init__(
            argument_spec=argument_spec,
            supports_check_mode=True,
        )

    def run(self):
        task_id = None
        pool = self.tatlin.get_pool(self.params['pool'])

        if pool is None:
            self.fail_json(
                changed=False,
                error='Pool not found',
                msg='Port {0} was not found'.format(self.params['pool']),
            )

        if pool.provision == 'thick' and self.params['warning_threshold'] is not None:
            self.fail_json(
                changed=False,
                error='Prohibited parameter',
                msg='warning_threshold argument is forbidden '
                    'for pool with thick provision',
            )

        suffixes = self.get_name_suffixes()
        all_resources = pool.get_resources()

        changed_names = []
        all_changes = self.get_all_changes(all_resources, suffixes)
        if len(all_changes) > 0:
            if not self.check_mode:
                for resource, changes in all_changes:
                    resource.update(**changes)

            self.changed = True
            for resource, changes in all_changes:
                changed_names.append(resource.name)

        missing_name, name_template, new_names = \
            self.get_missing_names_with_template(all_resources, suffixes)

        if missing_name is not None:
            ports = self.get_requested_ports()
            hosts = self.get_requested_hosts()
            host_groups = self.get_requested_host_groups()

            if not self.check_mode:
                task_id = pool.create_resource_block(
                    name=missing_name,
                    size=self.params['size'],
                    size_format=self.params['size_format'],
                    name_template=name_template,
                    read_cache=self.params['read_cache'],
                    write_cache=self.params['write_cache'],
                    warning_threshold=self.params['warning_threshold'],
                    ports=ports,
                    hosts=hosts,
                    host_groups=host_groups,
                )
            self.changed = True

        if self.params['wait'] and task_id is not None:
            self.wait_for_task_completion(task_id)

        if self.changed:
            result_msg = 'Operation successful'
        else:
            result_msg = 'No changes required'

        self.exit_json(
            msg=result_msg,
            changed=self.changed,
            created_resources=new_names,
            changed_resources=changed_names,
        )

    def get_all_changes(self, all_resources, suffixes):
        rv = []

        base_name = self.params['name']
        desired_names = [base_name + s for s in suffixes] or [base_name]

        for resource in all_resources:
            if resource.name in desired_names:
                changes = self.get_single_changes(resource)
                if len(changes) > 0:
                    rv.append((resource, changes))

        return rv

    def get_missing_names_with_template(self, all_resources, suffixes):
        missing_suffixes = []

        base_name = self.params['name']
        new_names = [base_name + s for s in suffixes]
        old_names = [res.name for res in all_resources]

        for new_name, suffix in zip(new_names, suffixes):
            if new_name not in old_names:
                missing_suffixes.append(suffix)

        if len(missing_suffixes) == 1:
            new_resource_name = base_name + missing_suffixes[0]
            return new_resource_name, None, [new_resource_name]
        elif len(missing_suffixes) > 1:
            new_resources_names = [
                base_name + suffix for suffix in missing_suffixes
            ]

            return (
                base_name,
                self.generate_template(missing_suffixes),
                new_resources_names,
            )
        else:
            return None, None, []

    @staticmethod
    def generate_template(suffixes):
        template = ''

        for i, current_suffix in enumerate(suffixes):
            is_last = i == len(suffixes) - 1
            if is_last:
                template += current_suffix
            else:
                next_suffix = suffixes[i + 1]
                last_symbol = template[-1] if template else ''

                if int(next_suffix) - int(current_suffix) == 1 and last_symbol != '-':
                    template += current_suffix + '-'
                elif int(next_suffix) - int(current_suffix) > 1:
                    template += current_suffix + ','

        return template

    def get_name_suffixes(self):
        name_template = self.params['name_template']
        if name_template is None:
            return ['']

        rv = []

        sub_templates = name_template.split(',')
        for sub_template in sub_templates:
            parts = sub_template.split('-')  # '1-3'/'1' -> ['1','3']/['1']
            if len(parts) < 2:
                parts *= 2  # ['1','3']/['1'] -> ['1','3']/['1','1']

            start, end = parts[:2]  # ['1','3']/['1','1'] -> ('1','3')/('1','1')

            try:
                suffix_range = range(int(start), int(end) + 1)
            except ValueError:
                self.fail_json(
                    changed=False,
                    error='Wrong template',
                    msg='There is an error in resource name template',
                )
                suffix_range = ()  # Just PyCharm satisfying

            for i in suffix_range:
                rv.append(str(i))

        return sorted(rv, key=int)

    def get_single_changes(self, resource):
        rv = {}

        if self.params['size'] is not None:
            old_size = resource.capacity_total
            new_size = self.params['size']

            if isinstance(new_size, str):
                new_size = to_bytes(new_size)

            if new_size != old_size:
                rv['size'] = self.params['size']

        new_read_cache = self.params['read_cache']
        old_read_cache = resource.read_cache
        if new_read_cache is not None and new_read_cache != old_read_cache:
            rv['read_cache'] = new_read_cache

        new_write_cache = self.params['write_cache']
        old_write_cache = resource.write_cache
        if new_write_cache is not None and new_write_cache != old_write_cache:
            rv['write_cache'] = new_write_cache

        new_warning = self.params['warning_threshold']
        old_warning = resource.warning_threshold
        if new_warning is not None and new_warning != old_warning:
            rv['warning_threshold'] = new_warning

        if self.params['ports'] is not None:
            new_ports = set(self.params['ports'])
            old_ports = set(p.name for p in resource.ports)
            if new_ports != old_ports:
                rv['ports'] = self.get_requested_ports()

        if self.params['hosts'] is not None:
            new_hosts = set(self.params['hosts'])
            old_hosts = set(h.name for h in resource.hosts)
            if new_hosts != old_hosts:
                rv['hosts'] = self.get_requested_hosts()

        if self.params['host_groups'] is not None:
            new_groups = set(self.params['host_groups'])
            old_groups = set(hg.name for hg in resource.host_groups)
            if new_groups != old_groups:
                rv['host_groups'] = self.get_requested_host_groups()

        return rv

    def get_requested_host_groups(self):
        if self.params['host_groups'] is None:
            return None

        rv = []

        groups = self._get_host_groups()
        for group_name in self.params['host_groups']:
            group = self.find_object_by_name(groups, group_name)

            if group is None:
                self.fail_json(
                    changed=False,
                    error='Host group not found',
                    msg='Host group {0} was not found'.format(group_name),
                )

            rv.append(group)

        return rv

    def get_requested_hosts(self):
        if self.params['hosts'] is None:
            return None

        rv = []

        hosts = self._get_hosts()
        for host_name in self.params['hosts']:
            host = self.find_object_by_name(hosts, host_name)

            if host is None:
                self.fail_json(
                    changed=False,
                    error='Host not found',
                    msg='Host {0} was not found'.format(host_name),
                )

            rv.append(host)

        return rv

    def get_requested_ports(self):
        if self.params['ports'] is None:
            return None

        rv = []

        ports = self._get_ports()
        for port_name in self.params['ports']:
            port = self.find_object_by_name(ports, port_name)

            if port is None:
                self.fail_json(
                    changed=False,
                    error='Port not found',
                    msg='Requested port {0} was not found'.format(port_name),
                )

            rv.append(port)

        return rv

    @staticmethod
    def find_object_by_name(obj_list, name):
        return next((obj for obj in obj_list if obj.name == name), None)

    def validate_params_create(self):
        if self.params['size'] is None:
            self.fail_json(
                changed=False,
                error='Missing required argument',
                msg='size argument is required for creating a new resource',
            )

    def validate_params_change(self, resource):
        old_size_format = resource.size_format
        new_size_format = self.params['size_format']
        if new_size_format and new_size_format != old_size_format:
            self.fail_json(
                changed=False,
                error='Changing forbidden parameter',
                msg='It is prohibited to change size_format. '
                    'Old value: {old_value}. '
                    'New value: {new_value}'.format(
                        old_value=old_size_format,
                        new_value=new_size_format),
            )

    def wait_for_task_completion(self, task_id):
        task = self.tatlin.get_task(task_id)
        start_time = time.time()

        while task.state != 'done':
            if time.time() - start_time > self.params['wait_timeout']:
                self.fail_json(
                    changed=True,
                    error='Timeout error',
                    msg='Task has not done state for {0} seconds'.format(
                        self.params['wait_timeout'],
                    ),
                )

            time.sleep(1)
            task.load()

            if task.state in ('error', 'aborting', 'aborted'):
                if task.state == 'error':
                    msg = 'Tatlin task was finished with error state'
                else:
                    msg = task.err_msg

                self.fail_json(
                    changed=True,
                    error='Tatlin task error',
                    msg=msg,
                )

    def _get_host_groups(self):
        if self._host_groups is None:
            self._host_groups = self.tatlin.get_host_groups()
        return self._host_groups

    def _get_hosts(self):
        if self._hosts is None:
            self._hosts = self.tatlin.get_hosts()
        return self._hosts

    def _get_ports(self):
        if self._ports is None:
            self._ports = self.tatlin.get_ports()
        return self._ports


def main():
    TatlinResourceBlockModule()


if __name__ == "__main__":
    main()
