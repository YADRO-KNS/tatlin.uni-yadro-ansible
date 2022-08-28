# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import json
from ansible_collections.yadro.tatlin.tests.unit.compat.mock import MagicMock
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import OPEN_URL_FUNC
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.tatlin_client import TatlinClient


@pytest.fixture()
def tatlin():
    return TatlinClient(
        base_url='localhost',
        username='admin',
        password='admin',
    )


@pytest.fixture
def make_mock(mocker):

    def f(target, return_value=None, side_effect=None, chain_calls=False):
        if return_value is None:
            return_value = {}

        if target == OPEN_URL_FUNC:
            return_value = _mock_open_url(return_value, chain_calls)

        mock = mocker.patch(
            target,
            side_effect=side_effect,
            return_value=return_value,
        )

        return mock

    def _mock_open_url(return_value, chain_calls):
        response_mock = MagicMock()
        if chain_calls and return_value is not None:
            gen = (json.dumps(d) for d in return_value)
            # Python 2 generators have next instead of __next__
            response_mock.read = gen.__next__ \
                if hasattr(gen, '__next__') else gen.next
        else:
            response_mock.read.return_value = json.dumps(return_value)
        return response_mock

    return f


@pytest.fixture
def open_url_kwargs():
    return {
        "method": 'GET',
        "url": "https://localhost",
        "data": None,
        "validate_certs": True,
        "use_proxy": True,
        "timeout": 60,
        "follow_redirects": "all",
        "headers": {},
        "force_basic_auth": False,
    }
