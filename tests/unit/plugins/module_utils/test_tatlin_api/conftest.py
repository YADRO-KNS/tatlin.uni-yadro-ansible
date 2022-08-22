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
def mock_method(mocker):

    def f(target, *args, **kwargs):
        # Python 2 does not support Keyword-Only Arguments (PEP 3102)
        side_effects = None
        if 'side_effects' in kwargs:
            side_effects = kwargs.pop('side_effects')

        if target == OPEN_URL_FUNC:
            response_mock = MagicMock()
            response_mock.read.return_value = json.dumps(args or kwargs)
        else:
            response_mock = args or kwargs

        mock = mocker.patch(
            target,
            side_effect=side_effects,
            return_value=response_mock,
        )

        return mock

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
