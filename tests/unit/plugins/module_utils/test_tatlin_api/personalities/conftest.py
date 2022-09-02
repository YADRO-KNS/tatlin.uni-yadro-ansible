# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest


@pytest.fixture
def hosts_data():
    return [
        {
            "version": "cdf087471cd7d0cbb7b8b2ab019ebe88",
            "id": "7ab276b8-59a3-416b-8f28-191e91b4e20b",
            "name": "testhost",
            "port_type": "iscsi",
            "initiators": [
                "iqn.1993-08.org.debian:01:5728e30474c"
            ],
            "tags": [
                "tag1",
                "tag2"
            ],
            "comment": "",
            "auth": {
                "internal_name": "hostname",
                "internal_password": "JLrGU-1qbCbb7XF1bFgEpkm2UatyH5H_EOrGIxs7BGE",
                "external_name": "targetname",
                "external_password": "Z5JJapsKhhkBwOIOfnHC34q0TCl2bmBjU_dnEeOECWo",
                "auth_type": "mutual"
            }
        },
        {
            "version": "41d0964c8d588d564a9122d888e6faa8",
            "id": "9355f65d-a8a2-4df9-8459-98a5c20725f3",
            "name": "host1",
            "port_type": "iscsi",
            "initiators": [],
            "tags": [
                "testtag"
            ],
            "comment": "",
            "auth": {
                "auth_type": "none"
            }
        },
    ]
