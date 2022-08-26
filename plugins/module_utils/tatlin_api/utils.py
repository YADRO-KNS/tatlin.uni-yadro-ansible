# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError


def to_bytes(s):  # type: (str) -> int
    units_dec = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    units_bin = ('B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB')

    last_digit = 0
    for char in s:
        if not (char.isdigit() or char == '.'):
            break
        last_digit += 1

    try:
        size = float(s[:last_digit])
    except ValueError:
        raise TatlinClientError(
            'Incorrect size value: ' + s
        )

    unit = s[last_digit:].strip() or 'B'

    if unit in units_dec:
        multiplier = 1000 ** units_dec.index(unit)
    elif unit in units_bin:
        multiplier = 1024 ** units_bin.index(unit)
    else:
        raise TatlinClientError(
            'Wrong size unit was passed: {0}. '
            'Allowed units: [{1}]'.format(
                unit, ', '.join(units_bin + units_dec))
        )

    return int((size * multiplier) + 0.5)
