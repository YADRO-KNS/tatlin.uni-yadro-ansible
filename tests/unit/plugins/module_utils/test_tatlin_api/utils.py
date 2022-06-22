# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from hamcrest import assert_that, has_item


def check_object(obj, exp_params):
    exp_params = exp_params if isinstance(exp_params, list) else [exp_params]
    fact_params = dict((k, v) for k, v in obj.__dict__.items()
                       if k in exp_params[0])
    assert_that(exp_params, has_item(fact_params))
