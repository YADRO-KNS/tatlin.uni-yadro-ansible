# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import (
    TatlinNodeNotFoundError, RESTClientNotFoundError)
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import REBOOT_ENDPOINT
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import OPEN_URL_FUNC


class TestRebootNode:

    @pytest.mark.parametrize(
        'node_name', ['sp-0', 'sp-1']
    )
    def test_reboot_node(self, tatlin, mock_method, open_url_kwargs, node_name):
        # Mock open_url without data
        open_url_mock = mock_method(target=OPEN_URL_FUNC)

        # Reboot node
        tatlin.reboot_node(node_name)

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(
                REBOOT_ENDPOINT.format(node=node_name)
            ),
        )

        # Result: open_url was called with expected parameters
        open_url_mock.assert_called_with(**open_url_kwargs)

    def test_reboot_non_existing_node(self, tatlin, mock_method, open_url_kwargs):
        # Mock open_url with not found error
        mock_method(target=OPEN_URL_FUNC, side_effects=RESTClientNotFoundError)

        # Reboot non-existing node
        # Result: TatlinNodeNotFoundError was raised
        with pytest.raises(TatlinNodeNotFoundError):
            tatlin.reboot_node('test-node')
