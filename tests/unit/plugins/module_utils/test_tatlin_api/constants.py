TATLIN_API_PACKAGE = 'ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api'

REST_CLIENT_MODULE = TATLIN_API_PACKAGE + '.rest_client'
REST_CLIENT_CLASS = REST_CLIENT_MODULE + '.RestClient'
OPEN_URL_FUNC = REST_CLIENT_MODULE + '.open_url'

AUTH_PACKAGE = TATLIN_API_PACKAGE + '.auth'
AUTH_SERVICE_CLASS = AUTH_PACKAGE + '.auth_service.AuthService'
USER_CLASS = AUTH_PACKAGE + '.user.User'
USER_GROUP_CLASS = AUTH_PACKAGE + '.group.UserGroup'
LDAP_CONFIG_CLASS = AUTH_PACKAGE + '.ldap_config.LdapConfig'

OSMGR_PACKAGE = TATLIN_API_PACKAGE + '.osmgr'
PORT_MODULE = OSMGR_PACKAGE + '.port'
PORT_CLASS = PORT_MODULE + '.Port'
NTP_MODULE = OSMGR_PACKAGE + '.ntp'
NTP_CONFIG_CLASS = NTP_MODULE + '.NtpConfig'

NOTIFICATION_PACKAGE = TATLIN_API_PACKAGE + '.notification'
SNMP_MODULE = NOTIFICATION_PACKAGE + '.snmp'
SNMP_CONFIG_CLASS = SNMP_MODULE + '.SnmpConfig'
