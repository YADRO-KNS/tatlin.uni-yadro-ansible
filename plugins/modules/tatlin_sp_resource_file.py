#!/usr/bin/python
# -*- coding: utf-8 -*-

# YADRO Tatlin Unified Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r"""
---
module: tatlin_sp_resource_file
short_description: Create or modify a file resource
version_added: "1.0.0"
description:
  - This module is intended to create new file resource/resources and
    change existing resource/resources
  - Multiple resources can be created at once
    with I(name_template) (For Tatlin>=2.7 only)
  - Supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin_uni.connection_options
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
      - Possible formats - '1-3', '1-3,4,7-10', '0-99'
      - Example - with I(name_template='1-3') and I(name='res_') 3 resources
        with names 'res_1', 'res_2', 'res_3' will be created
      - Not supported in Tatlin<=2.7
  type:
    required: True
    type: str
    choices: ['cifs', 'nfs']
    description: Type of the file resource
  size:
    required: False
    type: str
    description:
      - Resource volume
      - Required if new resource is creating
      - Not allowed for changing
      - Can be presented as a string number with postfix
        For example '100 MiB'. Following postfixes are allowed -
        [B, KB, MB, GB, TB, PB, EB, ZB, YB, KiB, MiB, GiB, TiB, PiB, EiB, ZiB, YiB]
      - If no postfix is passed, 'B' (bytes) will be used
  read_cache:
    required: False
    type: bool
    description:
      - Cache reading
      - Required for creating a new resource
  write_cache:
    required: False
    type: bool
    description:
      - Cache writing
      - Required for creating a new resource
  ports:
    required: False
    type: list
    elements: str
    description: List of names of the ports for export resources
  subnets:
    required: False
    type: list
    elements: str
    description: List of names of the subnets for export resources
  users:
    required: False
    type: list
    elements: dict
    description:
      - List of names of the users for export resources
        with corresponding permissions
    suboptions:
      name:
        required: True
        type: str
        description: Name of the user
      permissions:
        required: True
        type: str
        choices: ['r', 'rw']
        description: User`s permissions
  user_groups:
    required: False
    type: list
    elements: dict
    description:
      - List of names of the user groups for export resources
        with corresponding permissions
    suboptions:
      name:
        required: True
        type: str
        description: Name of the user group
      permissions:
        required: True
        type: str
        choices: ['r', 'rw']
        description: User group`s permissions
  wait:
    required: False
    type: bool
    default: True
    description:
      - Wait until resource or resources will be created or changed
      - If C(false), there is no guarantee that task will be
        successfully completed
      - Irrelevant for bulk resources changing
  wait_timeout:
    required: False
    type: int
    default: 300
    description: Number of seconds to wait when I(wait=true)
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
- name: Set single resource
  yadro.tatlin_uni.tatlin_sp_resource_file:
    connection: "{{ connection }}"
    name: example_resource
    pool: example_pool
    type: nfs
    size: 100 MiB
    read_cache: true
    write_cache: true
    ports:
      - p00
      - p01
    subnets:
      - example_subnet1
      - example_subnet2
    users:
      - name: example_user1
        permissions: rw
      - name: example_user2
        permissions: r
    user_groups:
      - name: example_user_group1
        permissions: r
      - name: example_user_group2
        permissions: rw

- name: Set multiple resources
  yadro.tatlin_uni.tatlin_sp_resource_file:
    connection: "{{ connection }}"
    name: example_resource
    name_template: 1-3,5,7-8
    pool: example_pool
    type: nfs
    size: 100 MiB
    read_cache: true
    write_cache: true
    ports:
      - p00
      - p01
    subnets:
      - example_subnet1
      - example_subnet2
    users:
      - name: example_user1
        permissions: rw
      - name: example_user2
        permissions: r
    user_groups:
      - name: example_user_group1
        permissions: r
      - name: example_user_group2
        permissions: rw

- name: Change single resource
  yadro.tatlin_uni.tatlin_sp_resource_file:
    connection: "{{ connection }}"
    name: example_resource
    pool: example_pool
    type: nfs
    read_cache: false
    write_cache: false
    ports:
      - p10
    subnets:
      - example_subnet2
      - example_subnet3
    users:
      - name: example_user2
        permissions: rw
      - name: example_user3
        permissions: r
    user_groups:
      - name: example_user_group2
        permissions: r
      - name: example_user_group3
        permissions: rw

- name: Change multiple resources
  yadro.tatlin_uni.tatlin_sp_resource_file:
    connection: "{{ connection }}"
    name: example_resource
    name_template: 1-100
    pool: example_pool
    type: nfs
    read_cache: false
    write_cache: false
    ports:
      - p10
    subnets:
      - example_subnet2
      - example_subnet3
    users:
      - name: example_user2
        permissions: rw
      - name: example_user3
        permissions: r
    user_groups:
      - name: example_user_group2
        permissions: r
      - name: example_user_group3
        permissions: rw
"""


from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_module import TatlinModule
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.exception import (
    WrongResourceNameTemplate,
)
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.utils import (
    get_resource_name_suffixes,
    generate_resource_name_template,
    to_bytes,
)


class TatlinResourceFileModule(TatlinModule):

    def __init__(self):
        argument_spec = {
            'name': {'type': 'str', 'required': True},
            'pool': {'type': 'str', 'required': True},
            'name_template': {'type': 'str', 'required': False},
            'type': {
                'type': 'str',
                'choices': ['nfs', 'cifs'],
                'required': True,
            },
            'size': {'type': 'str', 'required': False},
            'read_cache': {'type': 'bool', 'required': False},
            'write_cache': {'type': 'bool', 'required': False},
            'ports': {'type': 'list', 'elements': 'str', 'required': False},
            'subnets': {'type': 'list', 'elements': 'str', 'required': False},
            'users': {
                'type': 'list',
                'elements': 'dict',
                'required': False,
                'options': {
                    'name': {'type': 'str', 'required': True},
                    'permissions': {
                        'type': 'str',
                        'choices': ['r', 'rw'],
                        'required': True,
                    },
                }
            },
            'user_groups': {
                'type': 'list',
                'elements': 'dict',
                'required': False,
                'options': {
                    'name': {'type': 'str', 'required': True},
                    'permissions': {
                        'type': 'str',
                        'choices': ['r', 'rw'],
                        'required': True,
                    },
                }
            },
            'wait': {'type': 'bool', 'default': True, 'required': False},
            'wait_timeout': {'type': 'int', 'default': 300, 'required': False}
        }

        # Caching this objects, because there can be
        # too many identical queries with bulk update
        self._subnets = None
        self._users = None
        self._user_groups = None
        self._ports = None

        super(TatlinResourceFileModule, self).__init__(
            argument_spec=argument_spec,
            supports_check_mode=True,
        )

    def run(self):
        task = None
        pool = self.tatlin.get_pool(self.params['pool'])

        if pool is None:
            self.fail_json(
                changed=False,
                error='Pool not found',
                msg='Pool {0} was not found'.format(self.params['pool']),
            )

        try:
            suffixes = get_resource_name_suffixes(
                self.params['name_template']
            )
        except WrongResourceNameTemplate as e:
            self.fail_json(changed=False, error='Wrong template', msg=str(e))

        all_resources = pool.get_resources()

        changed_names = []
        all_changes = self.get_all_changes(all_resources, suffixes)
        if len(all_changes) > 0:
            if not self.check_mode:
                for resource, changes in all_changes:
                    task = resource.update(**changes)

            self.changed = True
            for resource, changes in all_changes:
                changed_names.append(resource.name)

        missing_name, name_template, new_names = \
            self.get_missing_names_with_template(all_resources, suffixes)

        if missing_name is not None:
            ports = self.get_requested_ports()
            subnets = self.get_requested_subnets()
            users = self.get_requested_users()
            user_groups = self.get_requested_user_groups()

            if not self.check_mode:
                task = pool.create_resource_file(
                    name=missing_name,
                    resource_type=self.params['type'],
                    size=self.params['size'],
                    name_template=name_template,
                    read_cache=self.params['read_cache'],
                    write_cache=self.params['write_cache'],
                    ports=ports,
                    subnets=subnets,
                    users=users,
                    user_groups=user_groups,
                )
            self.changed = True

        if self.params['wait'] and task is not None:
            try:
                task.wait_until_complete(timeout=self.params['wait_timeout'])
            except Exception as e:
                self.fail_json(
                    changed=True,
                    error=type(e).__name__,
                    msg=str(e),
                )

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
                self.validate_params_change(resource)
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
                generate_resource_name_template(missing_suffixes),
                new_resources_names,
            )
        else:
            return None, None, []

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

        if self.params['ports'] is not None:
            new_ports = set(self.params['ports'])
            old_ports = set(p.name for p in resource.ports)
            if new_ports != old_ports:
                rv['ports'] = self.get_requested_ports()

        if self.params['subnets'] is not None:
            new_subnets = set(self.params['subnets'])
            old_subnets = set(s.name for s in resource.subnets)
            if new_subnets != old_subnets:
                rv['subnets'] = self.get_requested_subnets()

        if self.params['users'] is not None:
            new_users_and_permissions = self.get_requested_users()
            old_users_and_permissions = [(
                user, resource.get_user_permissions(user),
            ) for user in resource.users]

            new_users_and_permissions.sort(key=lambda x: x[0].name)
            old_users_and_permissions.sort(key=lambda x: x[0].name)

            if old_users_and_permissions != new_users_and_permissions:
                rv['users'] = new_users_and_permissions

        if self.params['user_groups'] is not None:
            new_groups_and_permissions = self.get_requested_user_groups()
            old_groups_and_permissions = [(
                group, resource.get_user_group_permissions(group),
            ) for group in resource.user_groups]

            new_groups_and_permissions.sort(key=lambda x: x[0].name)
            old_groups_and_permissions.sort(key=lambda x: x[0].name)

            if old_groups_and_permissions != new_groups_and_permissions:
                rv['user_groups'] = new_groups_and_permissions

        return rv

    def get_requested_ports(self):
        if self.params['ports'] is None:
            return None

        rv = []

        ports = self._get_ports()
        for name in self.params['ports']:
            port = self.find_object_by_name(ports, name)

            if port is None:
                self.fail_json(
                    changed=False,
                    error='Port not found',
                    msg='Requested port {0} was not found'.format(name),
                )

            rv.append(port)

        return rv

    def get_requested_subnets(self):
        if self.params['subnets'] is None:
            return None

        rv = []

        subnets = self._get_subnets()
        for name in self.params['subnets']:
            subnet = self.find_object_by_name(subnets, name)

            if subnet is None:
                self.fail_json(
                    changed=False,
                    error='Subnet not found',
                    msg='Requested subnet {0} was not found'.format(name),
                )
            rv.append(subnet)

        return rv

    def get_requested_user_groups(self):
        if self.params['user_groups'] is None:
            return None

        rv = []

        user_groups = self._get_user_groups()
        for name_permissions in self.params['user_groups']:
            name = name_permissions['name']
            permissions = name_permissions['permissions']
            group = self.find_object_by_name(user_groups, name)

            if group is None:
                self.fail_json(
                    changed=False,
                    error='User group not found',
                    msg='Requested user group {0} was not found'.format(name),
                )

            rv.append((group, permissions))

        return rv

    def get_requested_users(self):
        if self.params['users'] is None:
            return None

        rv = []

        users = self._get_users()
        for name_permissions in self.params['users']:
            name = name_permissions['name']
            permissions = name_permissions['permissions']
            user = self.find_object_by_name(users, name)

            if user is None:
                self.fail_json(
                    changed=False,
                    error='User not found',
                    msg='Requested user {0} was not found'.format(name),
                )

            rv.append((user, permissions))

        return rv

    @staticmethod
    def find_object_by_name(obj_list, name):
        return next((obj for obj in obj_list if obj.name == name), None)

    def validate_params_create(self):
        missing_args = []
        for param_name in ('type', 'size', 'read_cache', 'write_cache'):
            if self.params[param_name] is None:
                missing_args.append(param_name)

        if len(missing_args) > 0:
            self.fail_json(
                changed=False,
                error='Missing required arguments',
                msg='{0} arguments required for creating a new resource, '
                    'but have no values'.format(', '.join(missing_args)),
            )

    def validate_params_change(self, resource):
        err_args = []

        new_type = self.params['type']
        old_type = resource.type
        if new_type is not None and new_type != old_type:
            err_args.append('type')

        new_size = self.params['size']
        old_size = resource.capacity_total
        if new_size is not None and to_bytes(new_size) != old_size:
            err_args.append('size')

        if len(err_args) > 0:
            self.fail_json(
                changed=False,
                error='Changing forbidden parameter',
                msg='It is not allowed to change following '
                    'parameters: {0}'.format(', '.join(err_args))
            )

    def _get_ports(self):
        if self._ports is None:
            self._ports = self.tatlin.get_ports()
        return self._ports

    def _get_subnets(self):
        if self._subnets is None:
            self._subnets = self.tatlin.get_subnets()
        return self._subnets

    def _get_users(self):
        if self._users is None:
            self._users = self.tatlin.get_users()
        return self._users

    def _get_user_groups(self):
        if self._user_groups is None:
            self._user_groups = self.tatlin.get_user_groups()
        return self._user_groups


def main():
    TatlinResourceFileModule()


if __name__ == "__main__":
    main()
