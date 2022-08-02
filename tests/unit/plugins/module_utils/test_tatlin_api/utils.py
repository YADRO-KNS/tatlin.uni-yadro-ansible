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


def check_obj(objects, exp_params, ignore_order=None):
    """Check objects attributes

    Args:
        objects(object, list[object]): Object or list of objects, which
            will be checked
        exp_params(dict, list): Expected object parameters. May be a list
            if it's required to check multiple objects
        ignore_order(str, list): If passed, listed parameters will be compared
            without order. Actual for lists only. Can resort initial values,
            so be careful, if you want to use objects or expected parameters
            after such checking

        Note:
            All entry in exp_params should have same keys, because keys for
            checking are chosen from first entry in exp_params
    """

    exp_params_list = exp_params \
        if isinstance(exp_params, list) else [exp_params]

    objects = objects if isinstance(objects, list) else [objects]
    fact_params_list = [
        dict((k, v) for k, v in obj.__dict__.items()
             if k in exp_params_list[0]) for obj in objects
    ]

    if ignore_order is not None:
        ignore_order = ignore_order \
            if isinstance(ignore_order, list) else [ignore_order]

        def sortkey(element):
            if isinstance(element, dict):
                element = sorted(element.items())
            return repr(element)

        for exp_item, fact_item in zip(exp_params_list, fact_params_list):
            for param in ignore_order:
                if not isinstance(exp_item[param], list) \
                        or not isinstance(fact_item[param], list):
                    raise TypeError(
                        'Parameter for ignoring order must be a list. '
                        '{0} is not a list'.format(exp_item[param])
                    )

                exp_item[param].sort(key=sortkey)
                fact_item[param].sort(key=sortkey)

    for fact_params in fact_params_list:
        assert_that(exp_params_list, has_item(fact_params))


def check_called_with(mock, **exp_call_params):
    """
    open_url sends data to Tatlin in json format, and it requires dict keys in
    specific order. In most cases we don't need any order. Besides, Python 2
    doesn't have ordered dicts, so we have to retrieve request's dict from
    json manually. To avoid this and to reduce code in tests this checker was
    written
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
