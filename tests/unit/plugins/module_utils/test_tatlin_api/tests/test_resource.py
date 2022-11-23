# -*- coding: utf-8 -*-

# YADRO Tatlin Unified Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import json
import ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.endpoints as eps
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.exception import TatlinClientError
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.models.host_group import HostGroup
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.models.host import Host
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.models.pool import Pool
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.models.port import Port
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.models.subnet import Subnet
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.models.user import User
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.models.user_group import UserGroup
from ansible_collections.yadro.tatlin_uni.plugins.module_utils.tatlin_api.models.resource import (
    ResourceBlock, ResourceFile,
)
from ansible_collections.yadro.tatlin_uni.tests.unit.plugins.module_utils.test_tatlin_api.utils import check_called_with
from ansible_collections.yadro.tatlin_uni.tests.unit.plugins.module_utils.test_tatlin_api.constants import (
    OPEN_URL_FUNC,
    RESOURCE_BLOCK_CLASS,
    RESOURCE_FILE_CLASS,
    TATLIN_API_CLIENT_CLASS,
    POOL_MODULE,
)


class TestResource:

    def test_create_resources_block(
        self,
        tatlin,
        make_mock,
        mocker,
        open_url_kwargs,
        ports_data,
    ):
        pool_id = 'pool_id'

        # Create Pool object
        pool = Pool(
            client=tatlin,
            drive_group=None,
            thinProvision=True,
            id=pool_id,
        )

        # Create Port object
        port_data = next(data for data in ports_data
                         if data['id'] == 'p01')

        port = Port(client=tatlin, port_data=port_data)

        # Create Host object
        host = Host(client=tatlin, id='host_id', name='host_name')

        # Create HostGroup object
        host_group = HostGroup(
            client=tatlin, id='host_group_id', name='host_group_name',
        )

        # Mock open_url
        open_url_mock = make_mock(
            OPEN_URL_FUNC,
            return_value=[
                ['new_resource1',
                 'new_resource3',
                 'new_resource4',
                 'new_resource5'],
                {'id': 1}],
            chain_calls=True,
        )

        # Create resources
        task = pool.create_resource_block(
            name='new_resource',
            size='10 MiB',
            size_format='4kn',
            name_template='1,3-5',
            read_cache=False,
            write_cache=False,
            warning_threshold=69,
            ports=[port],
            hosts=[host],
            host_groups=[host_group],
        )

        # Defining expected call parameters
        calls = []
        common_req_params = {  # same params for both requests
            'poolId': pool_id,
            'size': 10485760,
            'lbaFormat': '4kn',
            'cached': 'true',
            'rCacheMode': 'disabled',
            'wCacheMode': 'disabled',
            'alert_threshold': 69,
            'ports': ['p01'],
            'hosts': ['host_name'],
            'groups': ['host_group_name'],
        }

        # Define expected params for first call
        call_args1 = open_url_kwargs.copy()
        req_data = {
            'templates': [{
                'nameTemplate': 'new_resource',
                'params': '1,3-5',
            }]
        }
        req_data.update(common_req_params)

        call_args1.update(
            method='POST',
            headers={'Content-Type': 'application/json'},
            url='https://localhost/{0}'.format(
                eps.DASHBOARD_RESOURCES_ENDPOINT + '/block/create',
            ),
            data=req_data,
        )
        calls.append(mocker.call(**call_args1))

        # Define expected params for second call
        call_args2 = open_url_kwargs.copy()
        req_data = {
            'names': [
                'new_resource1',
                'new_resource3',
                'new_resource4',
                'new_resource5',
            ]
        }
        req_data.update(common_req_params)

        call_args2.update(
            method='PUT',
            headers={'Content-Type': 'application/json'},
            url='https://localhost/{0}'.format(
                eps.DASHBOARD_RESOURCES_ENDPOINT + '/block/create',
            ),
            data=req_data,
        )
        calls.append(mocker.call(**call_args2))

        # Python 2 has unordered dicts, so 'data' in open_url, which has json
        # format. To make comparison correct for Python 2 we substitute 'data'
        # field by dict
        for call_args in open_url_mock.call_args_list:
            if call_args.kwargs['data'] is not None:
                call_args.kwargs['data'] = json.loads(
                    call_args.kwargs['data']
                )

        # Result: Calls with expected params was sent
        open_url_mock.assert_has_calls(calls=calls, any_order=True)

        # Result: Expected task_id was returned
        assert task.id == 1

    @pytest.mark.parametrize('resource_type', ['nfs', 'cifs'])
    def test_create_resources_file(
        self,
        tatlin,
        make_mock,
        mocker,
        open_url_kwargs,
        ports_data,
        resource_type,
    ):
        pool_id = 'pool_id'

        # Create Pool object
        pool = Pool(
            client=tatlin,
            drive_group=None,
            thinProvision=True,
            id=pool_id,
        )

        # Create Port object
        port_data = next(data for data in ports_data
                         if data['id'] == 'p01')

        port = Port(client=tatlin, port_data=port_data)

        # Create Subnet object
        subnet = Subnet(client=tatlin, id='subnet_id', name='subnet_name')

        # Create User object
        user = User(
            client=tatlin,
            name='user_name',
            uid='uid',
            enabled=True,
            member_of=[],
        )

        # Create UserGroup object
        user_group = UserGroup(client=tatlin, name='group_name', gid='gid')

        # Mock open_url
        open_url_mock = make_mock(
            OPEN_URL_FUNC,
            return_value=[
                {'tatlin-version': {'L2': '2.7.0-123'}},
                ['new_resource1',
                 'new_resource2',
                 'new_resource3',
                 'new_resource5',
                 'new_resource8',
                 'new_resource9',
                 'new_resource10'],
                {'id': 2}],
            chain_calls=True,
        )

        # Create resources
        task = pool.create_resource_file(
            name='new_resource',
            resource_type=resource_type,
            size='100 MiB',
            name_template='1-3, 5,8-10',
            read_cache=False,
            write_cache=False,
            ports=[port],
            subnets=[subnet],
            users=[(user, 'rw')],
            user_groups=[(user_group, 'r')],
        )

        # Defining expected call parameters
        calls = []
        common_req_params = {  # same params for both requests
            'type': resource_type,
            'poolId': pool_id,
            'size': 104857600,
            'cached': 'true',
            'rCacheMode': 'disabled',
            'wCacheMode': 'disabled',
            'ports': [{'port': 'p01'}],
            'acl': [
                {'principal': {'kind': 'user', 'name': 'user_name'},
                 'permissions': ['read', 'write']},
                {'principal': {'kind': 'group', 'name': 'group_name'},
                 'permissions': ['read']},
            ],
            'subnets': ['subnet_id'],
        }

        # Define expected params for first call
        call_args1 = open_url_kwargs.copy()
        req_data = {
            'bulk_params': {
                'names': None,
                'templates': [{
                    'nameTemplate': 'new_resource',
                    'params': '1-3, 5,8-10',
                }],
            }
        }
        req_data.update(common_req_params)

        call_args1.update(
            method='POST',
            headers={'Content-Type': 'application/json'},
            url='https://localhost/{0}'.format(
                eps.DASHBOARD_RESOURCES_ENDPOINT + '/file/create',
            ),
            data=req_data,
        )
        calls.append(mocker.call(**call_args1))

        # Define expected params for second call
        call_args2 = open_url_kwargs.copy()
        req_data = {
            'bulk_params': {
                'names': [
                    'new_resource1',
                    'new_resource2',
                    'new_resource3',
                    'new_resource5',
                    'new_resource8',
                    'new_resource9',
                    'new_resource10'
                ]
            }
        }
        req_data.update(common_req_params)

        call_args2.update(
            method='PUT',
            headers={'Content-Type': 'application/json'},
            url='https://localhost/{0}'.format(
                eps.DASHBOARD_RESOURCES_ENDPOINT + '/file/create',
            ),
            data=req_data,
        )
        calls.append(mocker.call(**call_args2))

        # Python 2 has unordered dicts, so 'data' in open_url, which has json
        # format. To make comparison correct for Python 2 we substitute 'data'
        # field by dict
        for call_args in open_url_mock.call_args_list:
            if call_args.kwargs['data'] is not None:
                call_args.kwargs['data'] = json.loads(
                    call_args.kwargs['data']
                )

        # Result: Calls with expected params was sent
        open_url_mock.assert_has_calls(calls=calls, any_order=True)

        # Result: Expected task_id was returned
        assert task.id == 2

    @pytest.mark.parametrize('resource_type', ['nfs', 'cifs'])
    def test_create_resource_file_legacy(
        self,
        tatlin,
        make_mock,
        mocker,
        open_url_kwargs,
        ports_data,
        resource_type,
    ):
        # Mock uuid4
        make_mock(POOL_MODULE + '.uuid4', return_value='uuid')

        pool_id = 'pool_id'

        # Create Pool object
        pool = Pool(
            client=tatlin,
            drive_group=None,
            thinProvision=True,
            id=pool_id,
        )

        # Create Port object
        port_data = next(data for data in ports_data
                         if data['id'] == 'p01')

        port = Port(client=tatlin, port_data=port_data)

        # Create Subnet object
        subnet = Subnet(client=tatlin, id='subnet_id', name='subnet_name')

        # Create User object
        user = User(
            client=tatlin,
            name='user_name',
            uid='uid',
            enabled=True,
            member_of=[],
        )

        # Create UserGroup object
        user_group = UserGroup(client=tatlin, name='group_name', gid='gid')

        # Mock open_url
        open_url_mock = make_mock(
            OPEN_URL_FUNC,
            return_value=[
                {'tatlin-version': {'L2': '2.6.0-123'}},
                {'id': 3}],
            chain_calls=True,
        )

        # Create resources
        task = pool.create_resource_file(
            name='new_resource',
            resource_type=resource_type,
            size='100 MiB',
            read_cache=True,
            write_cache=True,
            ports=[port],
            subnets=[subnet],
            users=[(user, 'rw')],
            user_groups=[(user_group, 'r')],
        )

        calls = []

        # Define expected params for first call
        call_args1 = open_url_kwargs.copy()
        call_args1.update(
            method='GET',
            url='https://localhost/{0}'.format(eps.SYSTEM_VERSION_ENDPOINT),
        )
        calls.append(mocker.call(**call_args1))

        # Define expected params for second call
        call_args2 = open_url_kwargs.copy()
        call_args2.update(
            method='PUT',
            headers={'Content-Type': 'application/json'},
            url='https://localhost/{0}'.format(
                eps.DASHBOARD_RESOURCES_ENDPOINT + '/file/create',
            ),
            data={
                'id': 'uuid',
                'name': 'new_resource',
                'type': resource_type,
                'poolId': pool_id,
                'size': 104857600,
                'cached': 'true',
                'rCacheMode': 'enabled',
                'wCacheMode': 'enabled',
                'ports': [{'port': 'p01'}],
                'acl': [
                    {'principal': {'kind': 'user', 'name': 'user_name'},
                     'permissions': ['read', 'write']},
                    {'principal': {'kind': 'group', 'name': 'group_name'},
                     'permissions': ['read']},
                ],
                'subnets': ['subnet_id'],
            },
        )
        calls.append(mocker.call(**call_args2))

        # Python 2 has unordered dicts, so 'data' in open_url, which has json
        # format. To make comparison correct for Python 2 we substitute 'data'
        # field by dict
        for call_args in open_url_mock.call_args_list:
            if call_args.kwargs['data'] is not None:
                call_args.kwargs['data'] = json.loads(
                    call_args.kwargs['data']
                )

        # Result: Calls with expected params was sent
        open_url_mock.assert_has_calls(calls=calls)

        # Result: Expected task_id was returned
        assert task.id == 3

    @pytest.mark.parametrize('resource_type', ['nfs', 'cifs'])
    def test_create_resource_file_legacy_fail(
        self,
        tatlin,
        make_mock,
        resource_type,
    ):
        """Tatlin 2.6 does not support bulk resources creation"""

        pool_id = 'pool_id'

        # Create Pool object
        pool = Pool(
            client=tatlin,
            drive_group=None,
            thinProvision=True,
            id=pool_id,
        )

        # Mock open_url
        make_mock(
            OPEN_URL_FUNC,
            return_value={'tatlin-version': {'L2': '2.6.0-123'}}
        )

        # Create resources
        # Result: Error was raised
        with pytest.raises(TatlinClientError):
            pool.create_resource_file(
                name='new_resource',
                resource_type=resource_type,
                size='100 MiB',
                name_template='1-3, 5,8-10',
                read_cache=False,
                write_cache=False,
            )

    def test_get_resources(
        self,
        tatlin,
        make_mock,
        ports_data,
        resources_data,
    ):
        host_id = 'host_id'
        host_name = 'test_host'
        host_group_id = 'host_group_id'
        host_group_name = 'test_host_group'

        # Create Pool object
        pool = Pool(
            client=tatlin,
            drive_group=None,
            thinProvision=True,
            id='28118216-74eb-4ba2-8e01-be894b878de1',
        )

        # Create Host object
        host = Host(client=tatlin, id=host_id, name=host_name)

        # Create HostGroup object
        host_group = HostGroup(
            client=tatlin, id=host_group_id, name=host_group_name,
        )

        # Mock open_url with resources data
        make_mock(
            OPEN_URL_FUNC,
            return_value=resources_data,
        )

        # Get pool`s resources
        resources = pool.get_resources()

        # Result: Resources with expected parameter were returned
        assert resources[0].capacity_total == 1048576
        assert resources[0].capacity_used == 1048576
        assert resources[0].id == 'c66dbc61-6e79-425b-b2ae-e396fd06ee68'
        assert resources[0].name == 'test_block_resource1'
        assert resources[0].read_cache is True
        assert resources[0].size_format == '4kn'
        assert resources[0].status == 'ready'
        assert resources[0].type == 'block'
        assert resources[0].warning_threshold is None
        assert resources[0].write_cache is True

        assert resources[1].capacity_total == 2097152
        assert resources[1].capacity_used == 1048576
        assert resources[1].id == '48a75120-e8f9-42e7-8c42-2282047b4e3b'
        assert resources[1].name == 'test_block_resource2'
        assert resources[1].read_cache is False
        assert resources[1].size_format == '512e'
        assert resources[1].status == 'ready'
        assert resources[1].type == 'block'
        assert resources[1].warning_threshold == 70
        assert resources[1].write_cache is False

        assert resources[2].capacity_total == 104857600
        assert resources[2].capacity_used == 10485760
        assert resources[2].id == '4eae68d3-d793-4e08-972a-b64132e21f66'
        assert resources[2].name == 'test_file_resource1'
        assert resources[2].read_cache is True
        assert resources[2].size_format is None
        assert resources[2].status == 'ready'
        assert resources[2].type == 'nfs'
        assert resources[2].warning_threshold is None
        assert resources[2].write_cache is True

        assert resources[3].capacity_total == 104857600
        assert resources[3].capacity_used == 5242880
        assert resources[3].id == '187ca049-e0cd-4cd8-ac85-0c478a1f915a'
        assert resources[3].name == 'test_file_resource2'
        assert resources[3].read_cache is False
        assert resources[3].size_format is None
        assert resources[3].status == 'ready'
        assert resources[3].type == 'cifs'
        assert resources[3].warning_threshold is None
        assert resources[3].write_cache is False

        # Mock open_url with ports data
        make_mock(
            OPEN_URL_FUNC,
            return_value=ports_data,
        )

        # Get resource`s ports
        ports = resources[0].ports

        # Result: Resource has expected ports
        assert len(ports) == 1
        assert ports[0].name == 'p01'
        assert ports[0].type == 'ip'

        # Mock resource mapping
        make_mock(
            RESOURCE_BLOCK_CLASS + '._get_resources_mapping',
            return_value=[
                {'resource_id': resources[0].id,
                 'host_id': host.id,
                 'mapped_lun_id': 1},
                {'resource_id': resources[0].id,
                 'host_id': 'unnecessary_host_id',
                 'mapped_lun_id': 2},
                {'resource_id': resources[0].id,
                 'host_group_id': host_group.id,
                 'mapped_lun_id': 3},
                {'resource_id': resources[0].id,
                 'host_group_id': 'unnecessary_host_group_id',
                 'mapped_lun_id': 4},
            ]
        )

        # Mock get_hosts
        make_mock(
            TATLIN_API_CLIENT_CLASS + '.get_hosts',
            return_value=[host],
        )

        # Get resource`s hosts
        hosts = resources[0].hosts

        # Result: Expected hosts were returned
        assert len(hosts) == 1
        assert hosts[0].id == host_id
        assert hosts[0].name == host_name

        # Mock get_host_groups
        make_mock(
            TATLIN_API_CLIENT_CLASS + '.get_host_groups',
            return_value=[host_group]
        )

        # Get resource`s host_groups
        host_groups = resources[0].host_groups

        # Result: Expected host_groups were returned
        assert len(host_groups) == 1
        assert host_groups[0].id == host_group_id
        assert host_groups[0].name == host_group_name

    def test_get_resource(self, tatlin, make_mock, resources_data):
        # Create Pool object
        pool = Pool(
            client=tatlin,
            drive_group=None,
            thinProvision=True,
            id='28118216-74eb-4ba2-8e01-be894b878de1',
        )

        # Mock open_url with resources data
        make_mock(
            OPEN_URL_FUNC,
            return_value=resources_data,
        )

        # Get pool`s resource
        resource = pool.get_resource('test_block_resource1')

        # Result: Resources with expected parameter were returned
        assert resource.capacity_total == 1048576
        assert resource.capacity_used == 1048576
        assert resource.id == 'c66dbc61-6e79-425b-b2ae-e396fd06ee68'
        assert resource.name == 'test_block_resource1'
        assert resource.read_cache is True
        assert resource.size_format == '4kn'
        assert resource.status == 'ready'
        assert resource.type == 'block'
        assert resource.warning_threshold is None
        assert resource.write_cache is True

    def test_load_block(self, tatlin, make_mock, resources_data):
        # Create Pool object
        pool = Pool(
            client=tatlin,
            drive_group=None,
            thinProvision=True,
            id='28118216-74eb-4ba2-8e01-be894b878de1',
        )

        # Create empty ResourceBlock object
        resource = ResourceBlock(
            client=tatlin,
            pool=pool,
            id='c66dbc61-6e79-425b-b2ae-e396fd06ee68',
        )

        # Mock open_url with resources data
        make_mock(OPEN_URL_FUNC, return_value=resources_data[0])

        # Load resource
        resource.load()

        # Result: Resource has expected parameters
        assert resource.capacity_total == 1048576
        assert resource.capacity_used == 1048576
        assert resource.id == 'c66dbc61-6e79-425b-b2ae-e396fd06ee68'
        assert resource.name == 'test_block_resource1'
        assert resource.read_cache is True
        assert resource.size_format == '4kn'
        assert resource.status == 'ready'
        assert resource.type == 'block'
        assert resource.warning_threshold is None
        assert resource.write_cache is True

    def test_load_file(self, tatlin, make_mock, resources_data):
        # Create Pool object
        pool = Pool(
            client=tatlin,
            drive_group=None,
            thinProvision=True,
            id='28118216-74eb-4ba2-8e01-be894b878de1',
        )

        # Create empty ResourceFile object
        resource = ResourceFile(
            client=tatlin,
            pool=pool,
            id='4eae68d3-d793-4e08-972a-b64132e21f66',
        )

        # Mock open_url with resources data
        make_mock(
            OPEN_URL_FUNC,
            return_value=resources_data[2],
        )

        # Load resource
        resource.load()

        # Result: Resource has expected parameters
        assert resource.capacity_total == 104857600
        assert resource.capacity_used == 10485760
        assert resource.id == '4eae68d3-d793-4e08-972a-b64132e21f66'
        assert resource.name == 'test_file_resource1'
        assert resource.read_cache is True
        assert resource.size_format is None
        assert resource.status == 'ready'
        assert resource.type == 'nfs'
        assert resource.warning_threshold is None
        assert resource.write_cache is True

    def test_update_block(
        self,
        tatlin,
        make_mock,
        open_url_kwargs,
        ports_data,
        mocker,
    ):

        # Create Pool object
        pool = Pool(
            client=tatlin,
            drive_group=None,
            thinProvision=True,
            id='28118216-74eb-4ba2-8e01-be894b878de1',
        )

        # Create ResourceBlock object
        resource = ResourceBlock(
            client=tatlin,
            pool=pool,
            id='c66dbc61-6e79-425b-b2ae-e396fd06ee68',
            ports=[{'port': 'p10'}]
        )

        # Create Port objects
        port_to_add = Port(client=tatlin, port_data=next(
            data for data in ports_data if data['id'] == 'p01'))

        # Create Host objects
        host_to_add = Host(
            client=tatlin,
            id='host_to_add_id',
            name='host_to_add_name',
        )

        host_to_remove = Host(
            client=tatlin,
            id='host_to_remove_id',
            name='host_to_remove_name',
        )

        # Create HostGroup objects
        host_group_to_add = HostGroup(
            client=tatlin,
            id='host_group_to_add_id',
            name='host_group_add_name',
        )

        host_group_to_remove = HostGroup(
            client=tatlin,
            id='host_group_to_remove_id',
            name='host_group_remove_name',
        )

        # Mock host and group getters
        make_mock(
            TATLIN_API_CLIENT_CLASS + '.get_hosts',
            return_value=[host_to_add, host_to_remove],
        )

        make_mock(
            TATLIN_API_CLIENT_CLASS + '.get_host_groups',
            return_value=[
                host_group_to_add, host_group_to_remove
            ],
        )

        # Mock host and groups properties
        mocker.patch(
            RESOURCE_BLOCK_CLASS + '.hosts',
            new_callable=mocker.PropertyMock,
            return_value=[host_to_remove],
        )

        mocker.patch(
            RESOURCE_BLOCK_CLASS + '.host_groups',
            new_callable=mocker.PropertyMock,
            return_value=[host_group_to_remove],
        )

        # Mock open_url without data
        open_url_mock = make_mock(OPEN_URL_FUNC)

        # Mock load method
        make_mock(RESOURCE_BLOCK_CLASS + '.load')

        # Update resource
        resource.update(
            size='2 MiB',
            read_cache=True,
            write_cache=False,
            warning_threshold=69,
            ports=[port_to_add],
            hosts=[host_to_add],
            host_groups=[host_group_to_add],
        )

        calls = []

        # Define expected params for base update
        call_args1 = open_url_kwargs.copy()
        call_args1.update(
            method='POST',
            headers={'Content-Type': 'application/json'},
            url='https://localhost/{ep}/block/{id}'.format(
                ep=eps.PERSONALITIES_ENDPOINT,
                id=resource.id,
            ),
            data={
                'new_size': 2097152,
                'rCacheMode': 'enabled',
                'wCacheMode': 'disabled',
                'alert_threshold': 69,
            },
        )

        calls.append(mocker.call(**call_args1))

        # Define expected params for delete ports
        call_args2 = open_url_kwargs.copy()
        call_args2.update(
            method='DELETE',
            url='https://localhost/{ep}/block/{res_id}/ports/{port}'.format(
                ep=eps.PERSONALITIES_ENDPOINT,
                res_id=resource.id,
                port='p10',
            ),
        )

        calls.append(mocker.call(**call_args2))

        # Define expected params for put ports
        call_args3 = open_url_kwargs.copy()
        call_args3.update(
            method='PUT',
            url='https://localhost/{ep}/block/{res_id}/ports/{port}'.format(
                ep=eps.PERSONALITIES_ENDPOINT,
                res_id=resource.id,
                port=port_to_add.name,
            ),
        )

        calls.append(mocker.call(**call_args3))

        # Define expected params for delete hosts
        call_args4 = open_url_kwargs.copy()
        call_args4.update(
            method='DELETE',
            url='https://localhost/{ep}/block/{res_id}/hosts/{host}'.format(
                ep=eps.PERSONALITIES_ENDPOINT,
                res_id=resource.id,
                host=host_to_remove.id,
            ),
        )

        calls.append(mocker.call(**call_args4))

        # Define expected params for put ports
        call_args5 = open_url_kwargs.copy()
        call_args5.update(
            method='PUT',
            url='https://localhost/{ep}/block/{res_id}/hosts/{host}'.format(
                ep=eps.PERSONALITIES_ENDPOINT,
                res_id=resource.id,
                host=host_to_add.id,
            ),
        )

        calls.append(mocker.call(**call_args5))

        # Define expected params for delete hosts
        call_args6 = open_url_kwargs.copy()
        call_args6.update(
            method='DELETE',
            url='https://localhost/{ep}/block/{res_id}/groups/{group}'.format(
                ep=eps.PERSONALITIES_ENDPOINT,
                res_id=resource.id,
                group=host_group_to_remove.id,
            ),
        )

        calls.append(mocker.call(**call_args6))

        # Define expected params for put ports
        call_args7 = open_url_kwargs.copy()
        call_args7.update(
            method='PUT',
            url='https://localhost/{ep}/block/{res_id}/groups/{group}'.format(
                ep=eps.PERSONALITIES_ENDPOINT,
                res_id=resource.id,
                group=host_group_to_add.id,
            ),
        )

        calls.append(mocker.call(**call_args7))

        # Python 2 has unordered dicts, so 'data' in open_url, which has json
        # format. To make comparison correct for Python 2 we substitute 'data'
        # field by dict
        for call_args in open_url_mock.call_args_list:
            if call_args.kwargs['data'] is not None:
                call_args.kwargs['data'] = json.loads(
                    call_args.kwargs['data']
                )

        # Result: Calls with expected params was sent
        open_url_mock.assert_has_calls(calls=calls, any_order=True)

    def test_update_file(
        self,
        tatlin,
        make_mock,
        open_url_kwargs,
        ports_data,
        mocker,
    ):

        # Create Pool object
        pool = Pool(
            client=tatlin,
            drive_group=None,
            thinProvision=True,
            id='4eae68d3-d793-4e08-972a-b64132e21f66',
            ports=[{'port': 'p10'}],
        )

        # Create empty ResourceFile object
        resource = ResourceFile(
            client=tatlin,
            pool=pool,
            id='4eae68d3-d793-4e08-972a-b64132e21f66',
        )

        # Create Port objects
        port = Port(client=tatlin, port_data=next(
            data for data in ports_data if data['id'] == 'p01'))

        # Create Subnet object
        subnet = Subnet(client=tatlin, id='subnet_id', name='subnet_name')

        # Create User object
        user = User(
            client=tatlin,
            name='user_name',
            uid='uid',
            enabled=True,
            member_of=[],
        )

        # Create UserGroup object
        user_group = UserGroup(client=tatlin, name='group_name', gid='gid')

        # Mock open_url
        open_url_mock = make_mock(
            OPEN_URL_FUNC,
            return_value={'id': 1},
        )

        # Mock load method
        make_mock(RESOURCE_FILE_CLASS + '.load')

        # Update resource
        resource.update(
            read_cache=True,
            write_cache=False,
            ports=[port],
            subnets=[subnet],
            users=[(user, 'r')],
            user_groups=[(user_group, 'rw')],
        )

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            headers={'Content-Type': 'application/json'},
            url='https://localhost/{ep}/file/update/{id}'.format(
                ep=eps.DASHBOARD_RESOURCES_ENDPOINT,
                id='4eae68d3-d793-4e08-972a-b64132e21f66',
            ),
            data={
                'id': '4eae68d3-d793-4e08-972a-b64132e21f66',
                'rCacheMode': 'enabled',
                'wCacheMode': 'disabled',
                'ports': [{'port': 'p01'}],
                'subnets': [subnet.id],
                'acl': [
                    {'principal': {'kind': 'user', 'name': 'user_name'},
                     'permissions': ['read']},
                    {'principal': {'kind': 'group', 'name': 'group_name'},
                     'permissions': ['read', 'write']}
                ],
            }
        )

        check_called_with(open_url_mock, **open_url_kwargs)
