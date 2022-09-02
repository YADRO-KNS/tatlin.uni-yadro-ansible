# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.exception import TatlinClientError

try:
    from typing import Dict
except ImportError:
    Dict = None


ISCSI_AUTH_TYPES = ('none', 'oneway', 'mutual')


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


def get_iscsi_auth_for_request(
    auth,  # type: str
    username,  # type: str
    password,  # type: str
    mutual_username,  # type: str
    mutual_password,  # type: str
):  # type: (...) -> Dict[str, str]

    if auth not in ISCSI_AUTH_TYPES:
        raise TatlinClientError(
            'Unknown auth type: {0}'.format(auth)
        )

    rv = {'auth_type': auth}

    if auth in ('oneway', 'mutual'):
        if not username or not password:
            raise TatlinClientError(
                'username and password must be provided '
                'with auth type {0}'.format(auth)
            )

        rv.update(internal_name=username,
                  internal_password=password)

    if auth == 'mutual':
        if not all([
            username, password, mutual_username, mutual_password
        ]):
            raise TatlinClientError(
                'username, password, mutual_username and mutual_password '
                'must be provided with {0} auth type'.format(auth)
            )

        rv.update(external_name=mutual_username,
                  external_password=mutual_password)

    return rv
