# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
from hamcrest import assert_that, has_item, has_entries
from ansible_collections.yadro.tatlin.tests.unit.compat.mock import ANY


def check_object(obj, exp_params):
    exp_params = exp_params if isinstance(exp_params, list) else [exp_params]
    fact_params = dict((k, v) for k, v in obj.__dict__.items()
                       if k in exp_params[0])
    assert_that(exp_params, has_item(fact_params))


def check_called_with(mock, **exp_call_params):
    """
    Requests send data to Tatlin in json format and it requires dict keys in
    specific order. In most cases we don't need any order. Besides, Python 2
    doesn't have ordered dicts, so we need to retrieve request's doct from json
    manually. To avoid this and reduce code in tests this checker was written
    """

    if exp_call_params['data'] is not None:
        exp_data = exp_call_params['data']

        # Satisfy Python <= 2.7 & 3.5. It does not have builtin dict order,
        # so resulting json may be in different order than expected
        call_args, call_kwargs = mock.call_args
        call_data = json.loads(call_kwargs['data'])

        assert_that(call_data, has_entries(exp_data))

        exp_call_params['data'] = ANY

    mock.assert_called_with(**exp_call_params)
