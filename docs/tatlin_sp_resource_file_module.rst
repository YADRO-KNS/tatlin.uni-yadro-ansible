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

.. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

yadro.tatlin.tatlin_sp_resource_file module -- Create or modify a file resource
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `yadro.tatlin collection <https://galaxy.ansible.com/yadro/tatlin>`_ (version 1.0.0).

    You might already have this collection installed if you are using the ``ansible`` package.
    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install yadro.tatlin`.

    To use it in a playbook, specify: :code:`yadro.tatlin.tatlin_sp_resource_file`.

.. version_added

.. versionadded:: 1.0.0 of yadro.tatlin

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- This module is intended to create new file resource/resources and change existing resource/resources
- Multiple resources can be created at once with \ :emphasis:`name\_template`\  (For Tatlin>=2.7 only)
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
        <div class="ansibleOptionAnchor" id="parameter-connection"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-connection:

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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-connection/base_url:

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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-connection/login_path:

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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-connection/password:

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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-connection/timeout:

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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-connection/username:

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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-connection/validate_certs:

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
        <div class="ansibleOptionAnchor" id="parameter-name"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-name:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-name" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Name of the resource


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-name_template"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-name_template:

      .. rst-class:: ansible-option-title

      **name_template**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-name_template" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Template for bulk mode creation.

      Possible formats - '1-3', '1-3,4,7-10', '0-99'

      Example - with \ :emphasis:`name\_template='1-3'`\  and \ :emphasis:`name='res\_'`\  3 resources with names 'res_1', 'res_2', 'res_3' will be created

      Not supported in Tatlin<=2.7


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-pool"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-pool:

      .. rst-class:: ansible-option-title

      **pool**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-pool" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Name of the pool that includes the resource


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ports"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-ports:

      .. rst-class:: ansible-option-title

      **ports**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ports" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      List of names of the ports for export resources


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-read_cache"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-read_cache:

      .. rst-class:: ansible-option-title

      **read_cache**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-read_cache" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Cache reading

      Required for creating a new resource


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`no`
      - :ansible-option-choices-entry:`yes`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-size"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-size:

      .. rst-class:: ansible-option-title

      **size**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-size" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Resource volume

      Required if new resource is creating

      Not allowed for changing

      Can be presented as a string number with postfix For example '100 MiB'. Following postfixes are allowed - [B, KB, MB, GB, TB, PB, EB, ZB, YB, KiB, MiB, GiB, TiB, PiB, EiB, ZiB, YiB]

      If no postfix is passed, 'B' (bytes) will be used


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-subnets"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-subnets:

      .. rst-class:: ansible-option-title

      **subnets**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-subnets" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      List of names of the subnets for export resources


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-type"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-type:

      .. rst-class:: ansible-option-title

      **type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-type" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Type of the file resource


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`cifs`
      - :ansible-option-choices-entry:`nfs`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-user_groups"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-user_groups:

      .. rst-class:: ansible-option-title

      **user_groups**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-user_groups" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      List of names of the user groups for export resources with corresponding permissions


      .. raw:: html

        </div>
    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-user_groups/name"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-user_groups/name:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-user_groups/name" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Name of the user group


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-user_groups/permissions"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-user_groups/permissions:

      .. rst-class:: ansible-option-title

      **permissions**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-user_groups/permissions" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      User group`s permissions


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`r`
      - :ansible-option-choices-entry:`rw`

      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-users"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-users:

      .. rst-class:: ansible-option-title

      **users**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-users" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      List of names of the users for export resources with corresponding permissions


      .. raw:: html

        </div>
    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-users/name"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-users/name:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-users/name" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Name of the user


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-users/permissions"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-users/permissions:

      .. rst-class:: ansible-option-title

      **permissions**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-users/permissions" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      User`s permissions


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`r`
      - :ansible-option-choices-entry:`rw`

      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-wait"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-wait:

      .. rst-class:: ansible-option-title

      **wait**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-wait" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Wait until resource or resources will be created or changed

      If \ :literal:`false`\ , there is no guarantee that task will be successfully completed

      Irrelevant for bulk resources changing


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`no`
      - :ansible-option-default-bold:`yes` :ansible-option-default:`← (default)`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-wait_timeout"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-wait_timeout:

      .. rst-class:: ansible-option-title

      **wait_timeout**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-wait_timeout" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Number of seconds to wait when \ :emphasis:`wait=true`\ 


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`300`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-write_cache"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__parameter-write_cache:

      .. rst-class:: ansible-option-title

      **write_cache**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-write_cache" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Cache writing

      Required for creating a new resource


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`no`
      - :ansible-option-choices-entry:`yes`

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
    - name: Set single resource
      yadro.tatlin.tatlin_sp_resource_file:
        connection: "{{ connection }}"
        name: example_resource
        pool: example_pool
        type: nfs
        size: 100 MiB
        read_cache: true
        write_cache: true
        ports:
          - p00
          - p01
        subnets:
          - example_subnet1
          - example_subnet2
        users:
          - name: example_user1
            permissions: rw
          - name: example_user2
            permissions: r
        user_groups:
          - name: example_user_group1
            permissions: r
          - name: example_user_group2
            permissions: rw

    - name: Set multiple resources
      yadro.tatlin.tatlin_sp_resource_file:
        connection: "{{ connection }}"
        name: example_resource
        name_template: 1-3,5,7-8
        pool: example_pool
        type: nfs
        size: 100 MiB
        read_cache: true
        write_cache: true
        ports:
          - p00
          - p01
        subnets:
          - example_subnet1
          - example_subnet2
        users:
          - name: example_user1
            permissions: rw
          - name: example_user2
            permissions: r
        user_groups:
          - name: example_user_group1
            permissions: r
          - name: example_user_group2
            permissions: rw

    - name: Change single resource
      yadro.tatlin.tatlin_sp_resource_file:
        connection: "{{ connection }}"
        name: example_resource
        pool: example_pool
        type: nfs
        read_cache: false
        write_cache: false
        ports:
          - p10
        subnets:
          - example_subnet2
          - example_subnet3
        users:
          - name: example_user2
            permissions: rw
          - name: example_user3
            permissions: r
        user_groups:
          - name: example_user_group2
            permissions: r
          - name: example_user_group3
            permissions: rw

    - name: Change multiple resources
      yadro.tatlin.tatlin_sp_resource_file:
        connection: "{{ connection }}"
        name: example_resource
        name_template: 1-100
        pool: example_pool
        type: nfs
        read_cache: false
        write_cache: false
        ports:
          - p10
        subnets:
          - example_subnet2
          - example_subnet3
        users:
          - name: example_user2
            permissions: rw
          - name: example_user3
            permissions: r
        user_groups:
          - name: example_user_group2
            permissions: r
          - name: example_user_group3
            permissions: rw




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
        <div class="ansibleOptionAnchor" id="return-changed_resources"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__return-changed_resources:

      .. rst-class:: ansible-option-title

      **changed_resources**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-changed_resources" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Names of the changed resources


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` on success


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-created_resources"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__return-created_resources:

      .. rst-class:: ansible-option-title

      **created_resources**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-created_resources" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Names of the created resources


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` on success


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-error"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__return-error:

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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_resource_file_module__return-msg:

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

