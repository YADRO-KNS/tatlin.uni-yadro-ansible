# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class RESTClientError(Exception):
    pass


class RESTClientNotFoundError(Exception):
    pass


class RESTClientRequestError(Exception):
    pass


class RESTClientConnectionError(Exception):
    pass


class RESTClientUnauthorized(Exception):
    pass


class RESTClientBadRequest(Exception):
    pass


class TatlinClientError(Exception):
    pass
