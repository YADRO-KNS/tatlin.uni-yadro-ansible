REST_CLIENT_MODULE = 'ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.rest_client'
REST_CLIENT_CLASS = REST_CLIENT_MODULE + '.RestClient'
OPEN_URL_FUNC = REST_CLIENT_MODULE + '.open_url'
AUTH_PACKAGE = 'ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.auth'
AUTH_SERVICE_CLASS = AUTH_PACKAGE + '.auth_service.AuthService'
USER_CLASS = AUTH_PACKAGE + '.user.User'
USER_GROUP_CLASS = AUTH_PACKAGE + '.group.UserGroup'
LDAP_CONFIG_CLASS = AUTH_PACKAGE + '.ldap_config.LdapConfig'
