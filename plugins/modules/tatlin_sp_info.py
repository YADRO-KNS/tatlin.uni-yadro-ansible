#!/usr/bin/python
# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r"""
---
module: tatlin_sp_info
short_description: Get storage SP configuration
version_added: "1.0.0"
description:
  - Purpose of this module is to get storage
    SP configuration in a form of detailed inventory
  - This module supports check mode
author: "Sergey Kovalev (@kvlvs)"
extends_documentation_fragment:
  - yadro.tatlin.connection_options
"""

RETURN = r"""
---
msg:
  type: str
  returned: always
  description: Operation status message
error:
  type: str
  returned: on error
  description: Error details if raised
tatlin_info:
  type: dict
  description: Details of the system configuration
  returned: on success
  sample: {
   "system_name":"TU-SN-000000000000",
   "system_version":"2.6.0-151",
   "ports":{
      "mgmt":{
         "port_type":"ip",
         "gateway":"192.168.1.1",
         "mtu":1500,
         "virtual_address":"192.168.1.2/24",
         "mac":"None",
         "wwpn":"None",
         "nodes":{
            "sp-0":[{"ip":"192.168.1.3",
                     "mask":"24",
                     "status":"online"}],
            "sp-1":[{"ip":"192.168.1.4",
                     "mask":"24",
                     "status":"online"}]
         }
      },
      "p01":{
         "port_type":"ip",
         "gateway":"",
         "mtu":1500,
         "virtual_address":"None",
         "mac":{"sp-0":"00:00:00:00:00:00", "sp-1":"00:00:00:00:00:01"},
         "wwpn":"None",
         "nodes":{
            "sp-0":[{"ip":"192.168.1.5",
                     "mask":"24",
                     "status":"online"}],
            "sp-1":[{"ip":"192.168.1.3",
                     "mask":"24",
                     "status":"online"}]
         }
      }
   },
   "ldap":{
      "host":"192.168.0.10",
      "port":"389",
      "lookup_user":"cn=admin,dc=example,dc=com",
      "search_filter":"(memberof=cn=Users,dc=example,dc=com)",
      "base_dn":"dc=example,dc=com",
      "user_attribute":"cn",
      "group_attribute":"cn",
      "encryption":"off",
      "type":"custom"
   },
   "ntp":{"servers":["example.com", "127.0.0.1"]},
   "snmp":{
      "community":"tatlin",
      "servers":[{"ip":"example.com", "port":"162"}]
   },
   "smtp":{
      "address":"127.0.0.1",
      "encryption":"tls",
      "port":25,
      "sender":"smtp@example.com",
      "login":"admin",
      "recipients":["first@recipient.com", "second@recipient.com"]
   },
   "dns":{
      "servers":["127.0.0.1", "1.1.1.1"],
      "search_list":["test.example.com", "test.com"]
   },
   "syslog":{
      "recipients": [{"address":"127.0.0.1",
                      "port":"514",
                      "protocol":"udp",
                      "facility":10,
                      "severity":"critical",
                      "audit":false}]}
}
"""

EXAMPLES = r"""
---
- name: Get Tatlin info
  yadro.tatlin.tatlin_sp_info:
    connection: "{{ connection }}"
  register: result
"""


from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_module import TatlinModule


class TatlinInfoModule(TatlinModule):

    def __init__(self):
        super(TatlinInfoModule, self).__init__(
            supports_check_mode=True,
        )

    def run(self):
        tatlin_info = {
            'system_name': self.tatlin.system_name,
            'system_version': self.tatlin.system_version,
            'ports': self.get_ports_info(),
            'ldap': self.get_ldap_info(),
            'ntp': self.get_ntp_info(),
            'snmp': self.get_snmp_info(),
            'smtp': self.get_smtp_info(),
            'dns': self.get_dns_info(),
            'syslog': self.get_syslog_info(),
        }

        self.exit_json(
            msg="Operation successful.",
            tatlin_info=tatlin_info,
            changed=False,
        )

    def get_ports_info(self):
        ports = self.tatlin.get_ports()
        return dict(
            (port.name, {
                'port_type': port.type,
                'gateway': port.gateway,
                'mtu': port.mtu,
                'virtual_address': {
                    'ip': port.virtual_address.ip,
                    'mask': port.virtual_address.mask,
                } if port.virtual_address else None,
                'mac': port.mac,
                'wwpn': port.wwpn,
                'nodes': dict(
                    (node.name, [
                        {'ip': address.ip,
                         'mask': address.mask,
                         'status': address.status,
                         } for address in node.addresses
                    ]) for node in port.nodes.values())
            }) for port in ports
        )

    def get_ldap_info(self):
        ldap_config = self.tatlin.get_ldap_config()
        return {
            'host': ldap_config.host,
            'port': ldap_config.port,
            'lookup_user': ldap_config.lookup_user,
            'search_filter': ldap_config.search_filter,
            'base_dn': ldap_config.base_dn,
            'user_attribute': ldap_config.user_attribute,
            'group_attribute': ldap_config.group_attribute,
            'encryption': ldap_config.encryption,
            'type': ldap_config.type,
        }

    def get_ntp_info(self):
        ntp_config = self.tatlin.get_ntp_config()
        return {'servers': ntp_config.servers}

    def get_snmp_info(self):
        snmp_config = self.tatlin.get_snmp_config()

        servers = [
            {'ip': ip, 'port': port} for ip, port in (
                server.split(':') for server in snmp_config.servers
            )
        ]

        return {
            'community': snmp_config.community,
            'servers': servers,
        }

    def get_smtp_info(self):
        smtp_config = self.tatlin.get_smtp_config()
        return {
            'address': smtp_config.address,
            'encryption': smtp_config.encryption,
            'port': smtp_config.port,
            'sender': smtp_config.sender,
            'login': smtp_config.login,
            'recipients': smtp_config.recipients,
        }

    def get_dns_info(self):
        dns_config = self.tatlin.get_dns_config()
        return {
            'servers': dns_config.servers,
            'search_list': dns_config.search_list,
        }

    def get_syslog_info(self):
        syslog_config = self.tatlin.get_syslog_config()

        def lower_severity(recipient):
            rv = recipient.copy()
            rv['severity'] = rv['severity'].lower()
            return rv

        return {
            'recipients': [lower_severity(recipient)
                           for recipient in syslog_config.recipients]
        }


def main():
    TatlinInfoModule()


if __name__ == "__main__":
    main()
