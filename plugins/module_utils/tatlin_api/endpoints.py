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
CERTIFICATE_ENDPOINT = build_url(AUTH_ENDPOINT, 'certificate')


# Configuration service
CONFIGURATION_ENDPOINT = 'configuration'
PROPERTIES_ENDPOINT = build_url(CONFIGURATION_ENDPOINT, VERSION1, 'properties')
SYSTEM_NAME_ENDPOINT = build_url(PROPERTIES_ENDPOINT, 'system', 'name')


# Dashboard service
DASHBOARD_ENDPOINT = 'dashboard'
DASHBOARD_RESOURCES_ENDPOINT = build_url(DASHBOARD_ENDPOINT, VERSION1, 'resources')
DASHBOARD_TASKS_ENDPOINT = build_url(DASHBOARD_ENDPOINT, VERSION1, 'tasks')
DASHBOARD_SUBNETS_ENDPOINT = build_url(DASHBOARD_ENDPOINT, VERSION1, 'subnets')


# Health service
HEALTH_ENDPOINT = 'health'
HEALTH_MEDIAS_ENDPOINT = build_url(HEALTH_ENDPOINT, VERSION1, 'media')
HEALTH_POOLS_ENDPOINT = build_url(HEALTH_ENDPOINT, VERSION1, 'pools')
HEALTH_PERSONALITIES_ENDPOINT = build_url(
    HEALTH_ENDPOINT, VERSION1, 'personalities')


# Osmgr service
OSMGR_ENDPOINT = 'osmgr'
REBOOT_ENDPOINT = build_url(
    OSMGR_ENDPOINT, VERSION1, 'shutdown', '{node}', 'reboot')
PORTS_ENDPOINT = build_url(OSMGR_ENDPOINT, VERSION2, 'ports')
PORTS_STATUS_ENDPOINT = build_url(PORTS_ENDPOINT, 'status')
NETCONFIG_ENDPOINT = build_url(OSMGR_ENDPOINT, VERSION1, 'netconfig')
NTP_SERVERS_ENDPOINT = build_url(NETCONFIG_ENDPOINT, 'ntp', 'servers')
DNS_CONFIG_ENDPOINT = build_url(NETCONFIG_ENDPOINT, 'dns', 'resolver')


# Notification service
NOTIFICATION_ENDPOINT = 'notification'
SNMP_ENDPOINT = build_url(NOTIFICATION_ENDPOINT, VERSION1, 'handlers', 'snmp')
SMTP_ENDPOINT = build_url(NOTIFICATION_ENDPOINT, VERSION1, 'handlers', 'smtp')
SYSLOG_ENDPOINT = build_url(
    NOTIFICATION_ENDPOINT, VERSION1, 'handlers', 'syslog')


# Personalities service
PERSONALITIES_BASE_ENDPOINT = 'personalities'
PERSONALITIES_ENDPOINT = build_url(PERSONALITIES_BASE_ENDPOINT, VERSION1, 'personalities')
PERSONALITIES_BLOCK_ENDPOINT = build_url(PERSONALITIES_BASE_ENDPOINT, VERSION1, 'personalities', 'block')
PERSONALITIES_AUTH_ENDPOINT = build_url(PERSONALITIES_BLOCK_ENDPOINT, 'auth')
PERSONALITIES_CONFIG_ENDPOINT = build_url(PERSONALITIES_BASE_ENDPOINT, VERSION1, 'config')
PERSONALITIES_HOSTS_ENDPOINT = build_url(PERSONALITIES_CONFIG_ENDPOINT, 'hosts')
PERSONALITIES_HOST_GROUPS_ENDPOINT = build_url(PERSONALITIES_CONFIG_ENDPOINT, 'groups')
PERSONALITIES_RESOURCE_MAPPING_ENDPOINT = build_url(PERSONALITIES_CONFIG_ENDPOINT, 'resource_mapping')
PERSONALITIES_SUBNETS_ENDPOINT = build_url(PERSONALITIES_BASE_ENDPOINT, VERSION1, 'subnets')


# Upmgr service
UPMGR_ENDPOINT = 'upmgr'
SYSTEM_VERSION_ENDPOINT = build_url(UPMGR_ENDPOINT, VERSION1, 'version')
