.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. role:: ansible-attribute-support-label
.. role:: ansible-attribute-support-property
.. role:: ansible-attribute-support-full
.. role:: ansible-attribute-support-partial
.. role:: ansible-attribute-support-none
.. role:: ansible-attribute-support-na
.. role:: ansible-option-type
.. role:: ansible-option-elements
.. role:: ansible-option-required
.. role:: ansible-option-versionadded
.. role:: ansible-option-aliases
.. role:: ansible-option-choices
.. role:: ansible-option-choices-entry
.. role:: ansible-option-default
.. role:: ansible-option-default-bold
.. role:: ansible-option-configuration
.. role:: ansible-option-returned-bold
.. role:: ansible-option-sample-bold

.. Anchors

.. _ansible_collections.yadro.tatlin.tatlin_sp_info_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

yadro.tatlin.tatlin_sp_info module -- Get storage SP configuration
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `yadro.tatlin collection <https://galaxy.ansible.com/yadro/tatlin>`_ (version 1.0.0).

    You might already have this collection installed if you are using the ``ansible`` package.
    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install yadro.tatlin`.

    To use it in a playbook, specify: :code:`yadro.tatlin.tatlin_sp_info`.

.. version_added

.. versionadded:: 1.0.0 of yadro.tatlin

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Purpose of this module is to get storage SP configuration in a form of detailed inventory
- This module supports check mode


.. Aliases


.. Requirements






.. Options

Parameters
----------


.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-connection"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_info_module__parameter-connection:

      .. rst-class:: ansible-option-title

      **connection**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-connection" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      \ :emphasis:`connection`\  describes Tatlin Storage Processor (SP) connection configuration.

      Only session connection supported.

      Authorization is executed automatically with corresponding endpoint. 'auth/login' by default.

      Client receives x-auth-token and uses it for following requests.


      .. raw:: html

        </div>
    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-connection/base_url"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_info_module__parameter-connection/base_url:

      .. rst-class:: ansible-option-title

      **base_url**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-connection/base_url" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Tatlin REST API entrypoint.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-connection/login_path"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_info_module__parameter-connection/login_path:

      .. rst-class:: ansible-option-title

      **login_path**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-connection/login_path" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Tatlin REST API endpoint for authorization


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"auth/login"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-connection/password"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_info_module__parameter-connection/password:

      .. rst-class:: ansible-option-title

      **password**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-connection/password" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Tatlin user password.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-connection/timeout"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_info_module__parameter-connection/timeout:

      .. rst-class:: ansible-option-title

      **timeout**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-connection/timeout" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Tatlin REST API request timeout.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`60`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-connection/username"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_info_module__parameter-connection/username:

      .. rst-class:: ansible-option-title

      **username**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-connection/username" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Tatlin username to login.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-connection/validate_certs"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_info_module__parameter-connection/validate_certs:

      .. rst-class:: ansible-option-title

      **validate_certs**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-connection/validate_certs" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Responsible for SSL certificates validation.

      If set to False certificates won't validated.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`no`
      - :ansible-option-default-bold:`yes` :ansible-option-default:`← (default)`

      .. raw:: html

        </div>



.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Get Tatlin info
      yadro.tatlin.tatlin_sp_info:
        connection: "{{ connection }}"
      register: result




.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-error"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_info_module__return-error:

      .. rst-class:: ansible-option-title

      **error**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-error" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Error details if raised


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` on error


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-msg"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_info_module__return-msg:

      .. rst-class:: ansible-option-title

      **msg**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-msg" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Operation status message


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-tatlin_info"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_info_module__return-tatlin_info:

      .. rst-class:: ansible-option-title

      **tatlin_info**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-tatlin_info" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Details of the system configuration


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` on success

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` {"dns": {"search\_list": ["test.example.com", "test.com"], "servers": ["127.0.0.1", "1.1.1.1"]}, "ldap": {"base\_dn": "dc=example,dc=com", "encryption": "off", "group\_attribute": "cn", "host": "192.168.0.10", "lookup\_user": "cn=admin,dc=example,dc=com", "port": "389", "search\_filter": "(memberof=cn=Users,dc=example,dc=com)", "type": "custom", "user\_attribute": "cn"}, "ntp": {"servers": ["example.com", "127.0.0.1"]}, "ports": {"mgmt": {"gateway": "192.168.1.1", "mac": "None", "mtu": 1500, "nodes": {"sp-0": [{"ip": "192.168.1.3", "mask": "24", "status": "online"}], "sp-1": [{"ip": "192.168.1.4", "mask": "24", "status": "online"}]}, "port\_type": "ip", "virtual\_address": "192.168.1.2/24", "wwpn": "None"}, "p01": {"gateway": "", "mac": {"sp-0": "00:00:00:00:00:00", "sp-1": "00:00:00:00:00:01"}, "mtu": 1500, "nodes": {"sp-0": [{"ip": "192.168.1.5", "mask": "24", "status": "online"}], "sp-1": [{"ip": "192.168.1.3", "mask": "24", "status": "online"}]}, "port\_type": "ip", "virtual\_address": "None", "wwpn": "None"}}, "smtp": {"address": "127.0.0.1", "encryption": "tls", "login": "admin", "port": 25, "recipients": ["first@recipient.com", "second@recipient.com"], "sender": "smtp@example.com"}, "snmp": {"community": "tatlin", "servers": [{"ip": "example.com", "port": "162"}]}, "state\_hardware": "OK", "state\_security": "WARNING", "state\_storage": "ERROR", "syslog": {"recipients": [{"address": "127.0.0.1", "audit": false, "facility": 10, "port": "514", "protocol": "udp", "severity": "critical"}]}, "system\_name": "TU-SN-000000000000", "system\_version": "2.6.0-151"}


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Sergey Kovalev (@kvlvs)



.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. raw:: html

  <p class="ansible-links">
    <a href="TODO" aria-role="button" target="_blank" rel="noopener external">Issue Tracker</a>
    <a href="TODO" aria-role="button" target="_blank" rel="noopener external">Repository (Sources)</a>
  </p>

.. Parsing errors

