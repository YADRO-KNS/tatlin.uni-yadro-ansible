TATLIN_API_PACKAGE = 'ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api'

REST_CLIENT_MODULE = TATLIN_API_PACKAGE + '.rest_client'
REST_CLIENT_CLASS = REST_CLIENT_MODULE + '.RestClient'
OPEN_URL_FUNC = REST_CLIENT_MODULE + '.open_url'

AUTH_PACKAGE = TATLIN_API_PACKAGE + '.auth'
AUTH_SERVICE_CLASS = AUTH_PACKAGE + '.auth_service.AuthService'
USER_CLASS = AUTH_PACKAGE + '.user.User'
USER_GROUP_CLASS = AUTH_PACKAGE + '.group.UserGroup'
LDAP_CONFIG_CLASS = AUTH_PACKAGE + '.ldap_config.LdapConfig'

NETWORK_PACKAGE = TATLIN_API_PACKAGE + '.network'
PORT_MODULE = NETWORK_PACKAGE + '.port'
PORT_CLASS = PORT_MODULE + '.Port'