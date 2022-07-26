VERSION1 = 'v1'
VERSION2 = 'v2'


# Auth service
AUTH_ENDPOINT = 'auth'
USERS_ENDPOINT = '/'.join([AUTH_ENDPOINT, 'users'])
GROUPS_ENDPOINT = '/'.join([AUTH_ENDPOINT, 'groups'])
LDAP_ENDPOINT = '/'.join([AUTH_ENDPOINT, 'ldap'])
LDAP_CONFIG_ENDOPINT = '/'.join([LDAP_ENDPOINT, 'configuration'])


# Osmgr service
OSMGR_ENDPOINT = 'osmgr'
PORTS_ENDPOINT = '/'.join([OSMGR_ENDPOINT, VERSION2, 'ports'])
NETCONFIG_ENDPOINT = '/'.join([OSMGR_ENDPOINT, VERSION1, 'netconfig'])
NTP_SERVERS_ENDPOINT = '/'.join([NETCONFIG_ENDPOINT, 'ntp', 'servers'])
DNS_CONFIG_ENDPOINT = '/'.join([NETCONFIG_ENDPOINT, 'dns', 'resolver'])


# Notification service
NOTIFICATION_ENDPOINT = 'notification'
SNMP_ENDPOINT = '/'.join([NOTIFICATION_ENDPOINT, VERSION1, 'handlers', 'snmp'])
