# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.tatlin_client import TatlinClient


@pytest.fixture(scope='session')
def client():
    return TatlinClient(
        base_url='localhost',
        username='admin',
        password='admin',
    )


@pytest.fixture
def open_url_kwargs():
    return {
        "method": 'GET',
        "url": "https://localhost",
        "data": None,
        "validate_certs": True,
        "use_proxy": True,
        "timeout": 30,
        "follow_redirects": "all",
        "headers": {},
        "force_basic_auth": False,
    }
