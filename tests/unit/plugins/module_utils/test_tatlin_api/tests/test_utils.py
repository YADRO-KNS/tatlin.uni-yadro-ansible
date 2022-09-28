# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.utils import (
    get_resource_name_suffixes,
    generate_resource_name_template,
)


class TestUtils:

    @pytest.mark.parametrize(
        'name_template, exp_suffixes', [
            (None, ['']),
            ('1', ['1']),
            ('1,2', ['1', '2']),
            ('1-2', ['1', '2']),
            ('1-3', ['1', '2', '3']),
            ('99-101', ['99', '100', '101']),
            ('1-3, 5', ['1', '2', '3', '5']),
            ('3,5,7', ['3', '5', '7']),
            ('2, 5-7,10,11-13', ['2', '5', '6', '7', '10', '11', '12', '13']),
        ]
    )
    def test_get_resource_name_suffixes(self, name_template, exp_suffixes):
        fact_suffixes = get_resource_name_suffixes(name_template)
        assert fact_suffixes == exp_suffixes

    @pytest.mark.parametrize(
        'suffixes, exp_template', [
            ([], ''),
            (['1'], '1'),
            (['1', '2'], '1-2'),
            (['1', '2', '3'], '1-3'),
            (['99', '100', '101'], '99-101'),
            (['1', '2', '3', '5'], '1-3,5'),
            (['3', '5', '7'], '3,5,7'),
            (['2', '5', '6', '7', '10', '11', '12', '13'], '2,5-7,10-13')
        ]
    )
    def test_generate_resource_name_template(self, suffixes, exp_template):
        fact_template = generate_resource_name_template(suffixes)
        assert fact_template == exp_template
