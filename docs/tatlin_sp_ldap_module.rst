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

.. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

yadro.tatlin.tatlin_sp_ldap module -- Configure SP LDAP client settings.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `yadro.tatlin collection <https://galaxy.ansible.com/yadro/tatlin>`_ (version 1.0.0).

    You might already have this collection installed if you are using the ``ansible`` package.
    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install yadro.tatlin`.

    To use it in a playbook, specify: :code:`yadro.tatlin.tatlin_sp_ldap`.

.. version_added

.. versionadded:: 1.0.0 of yadro.tatlin

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- This module is intended to configure ldap settings for Storage Processor.
- Supports check mode


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
        <div class="ansibleOptionAnchor" id="parameter-base_dn"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__parameter-base_dn:

      .. rst-class:: ansible-option-title

      **base_dn**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-base_dn" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Ldap server's base dn for search


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-connection"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__parameter-connection:

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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__parameter-connection/base_url:

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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__parameter-connection/login_path:

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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__parameter-connection/password:

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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__parameter-connection/timeout:

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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__parameter-connection/username:

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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__parameter-connection/validate_certs:

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


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-crt_content"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__parameter-crt_content:

      .. rst-class:: ansible-option-title

      **crt_content**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-crt_content" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Content of ldap server's certificate

      Required if (I)encryption is (C)ssl or (C)tls

      Mutually exclusive with (I)crt_path


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-crt_path"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__parameter-crt_path:

      .. rst-class:: ansible-option-title

      **crt_path**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-crt_path" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Path to ldap server's certificate

      Required if (I)encryption is (C)ssl or (C)tls

      Mutually exclusive with (I)crt_content


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-encryption"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__parameter-encryption:

      .. rst-class:: ansible-option-title

      **encryption**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-encryption" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Encryption mode

      If ldap is encrypted ((C)ssl or (C)tls), certificate must be passed. If ldap was already configured as encrypted and one or several fields are updated (for example (I)search_filter) (I)crt_path or (I)crt_content must be passed. Otherwise an operation will be failed


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`ssl`
      - :ansible-option-choices-entry:`tls`
      - :ansible-option-choices-entry:`off`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-group_attribute"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__parameter-group_attribute:

      .. rst-class:: ansible-option-title

      **group_attribute**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-group_attribute" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Group attribute for search

      Prohibited if (I)type is (C)ad


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-host"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__parameter-host:

      .. rst-class:: ansible-option-title

      **host**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-host" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Ldap server's address


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-lookup_password"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__parameter-lookup_password:

      .. rst-class:: ansible-option-title

      **lookup_password**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-lookup_password" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Password for lookup user

      Required if (I)state is (C)present


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-lookup_user"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__parameter-lookup_user:

      .. rst-class:: ansible-option-title

      **lookup_user**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-lookup_user" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Name of lookup user


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-port"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__parameter-port:

      .. rst-class:: ansible-option-title

      **port**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-port" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Ldap server's port


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-search_filter"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__parameter-search_filter:

      .. rst-class:: ansible-option-title

      **search_filter**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-search_filter" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Filter in RFC 4515 format


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__parameter-state:

      .. rst-class:: ansible-option-title

      **state**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Ldap server's type


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`present` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`absent`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-type"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__parameter-type:

      .. rst-class:: ansible-option-title

      **type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-type" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Ldap server's type


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`ad`
      - :ansible-option-choices-entry:`custom`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-user_attribute"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__parameter-user_attribute:

      .. rst-class:: ansible-option-title

      **user_attribute**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-user_attribute" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      User attribute for search

      Prohibited if (I)type is (C)ad


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
    - name: Add ldap config
      yadro.tatlin.tatlin_sp_ldap:
        connection: "{{ connection }}"
        host: "{{ ldap_host }}"
        port: 389
        lookup_user: cn=admin,dc=example,dc=com
        lookup_password: password
        base_dn: dc=example,dc=com
        search_filter: "(memberof=cn=Users,dc=example,dc=com)"
        encryption: off
        user_attribute: cn
        group_attribute: cn
        type: custom

    - name: Change search filter
      yadro.tatlin.tatlin_sp_ldap:
        connection: "{{ connection }}"
        lookup_password: password
        search_filter: (uid=*)

    - name: Enable tls encryption
      yadro.tatlin.tatlin_sp_ldap:
        connection: "{{ connection }}"
        lookup_password: password
        encryption: tls
        port: 389
        crt_path: /path/to/certificate.pem

    - name: Add AD config with ssl encryption
      yadro.tatlin.tatlin_sp_ldap:
        connection: "{{ connection }}"
        host: "{{ ldap_host }}"
        port: 636
        lookup_user: cn=admin,dc=example,dc=com
        lookup_password: password
        base_dn: dc=example,dc=com
        search_filter: "(memberof=cn=Users,dc=example,dc=com)"
        encryption: ssl
        crt_content: |
          -----BEGIN CERTIFICATE-----
          MIIDuz...
        type: ad




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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__return-error:

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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_ldap_module__return-msg:

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

