# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


def build_url(*parts):
    return '/'.join(parts)


VERSION1 = 'v1'
VERSION2 = 'v2'


# Auth service
AUTH_ENDPOINT = 'auth'
USERS_ENDPOINT = build_url(AUTH_ENDPOINT, 'users')
GROUPS_ENDPOINT = build_url(AUTH_ENDPOINT, 'groups')
LDAP_ENDPOINT = build_url(AUTH_ENDPOINT, 'ldap')
LDAP_CONFIG_ENDOPINT = build_url(LDAP_ENDPOINT, 'configuration')


# Osmgr service
OSMGR_ENDPOINT = 'osmgr'
PORTS_ENDPOINT = build_url(OSMGR_ENDPOINT, VERSION2, 'ports')
NETCONFIG_ENDPOINT = build_url(OSMGR_ENDPOINT, VERSION1, 'netconfig')
NTP_SERVERS_ENDPOINT = build_url(NETCONFIG_ENDPOINT, 'ntp', 'servers')
DNS_CONFIG_ENDPOINT = build_url(NETCONFIG_ENDPOINT, 'dns', 'resolver')


# Notification service
NOTIFICATION_ENDPOINT = 'notification'
SNMP_ENDPOINT = build_url(NOTIFICATION_ENDPOINT, VERSION1, 'handlers', 'snmp')
SMTP_ENDPOINT = build_url(NOTIFICATION_ENDPOINT, VERSION1, 'handlers', 'smtp')
SYSLOG_ENDPOINT = build_url(NOTIFICATION_ENDPOINT, VERSION1, 'handlers', 'syslog')
