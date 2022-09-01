TATLIN_API_PACKAGE = 'ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api'
TATLIN_API_CLIENT_MODULE = TATLIN_API_PACKAGE + '.tatlin_client'
TATLIN_API_CLIENT_CLASS = TATLIN_API_CLIENT_MODULE + '.TatlinClient'


REST_CLIENT_MODULE = TATLIN_API_PACKAGE + '.rest_client'
REST_CLIENT_CLASS = REST_CLIENT_MODULE + '.RestClient'
OPEN_URL_FUNC = REST_CLIENT_MODULE + '.open_url'


MODELS_PACKAGE = TATLIN_API_PACKAGE + '.models'


DRIVE_GROUP_CLASS = MODELS_PACKAGE + '.drive_group.DriveGroup'
POOL_CLASS = MODELS_PACKAGE + '.pool.Pool'
RESOURCE_BLOCK_CLASS = MODELS_PACKAGE + '.resource.ResourceBlock'
RESOURCE_FILE_CLASS = MODELS_PACKAGE + '.resource.ResourceFile'


HOST_CLASS = MODELS_PACKAGE + '.host.Host'
HOST_GROUP_CLASS = MODELS_PACKAGE + '.host_group.HostGroup'


USER_CLASS = MODELS_PACKAGE + '.user.User'
USER_GROUP_CLASS = MODELS_PACKAGE + '.user_group.UserGroup'
LDAP_CONFIG_CLASS = MODELS_PACKAGE + '.ldap.LdapConfig'


PORT_CLASS = MODELS_PACKAGE + '.port.Port'
NTP_CONFIG_CLASS = MODELS_PACKAGE + '.ntp.NtpConfig'
DNS_CONFIG_CLASS = MODELS_PACKAGE + '.dns.DnsConfig'


SNMP_CONFIG_CLASS = MODELS_PACKAGE + '.snmp.SnmpConfig'
SMTP_CONFIG_CLASS = MODELS_PACKAGE + '.smtp.SmtpConfig'
SYSLOG_CONFIG_CLASS = MODELS_PACKAGE + '.syslog.SyslogConfig'
