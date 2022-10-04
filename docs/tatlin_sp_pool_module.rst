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

.. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

yadro.tatlin.tatlin_sp_pool module -- Create, modify or destroy a pool
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `yadro.tatlin collection <https://galaxy.ansible.com/yadro/tatlin>`_ (version 1.0.0).

    You might already have this collection installed if you are using the ``ansible`` package.
    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install yadro.tatlin`.

    To use it in a playbook, specify: :code:`yadro.tatlin.tatlin_sp_pool`.

.. version_added

.. versionadded:: 1.0.0 of yadro.tatlin

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- This module is intended to create new pool and change or remove existing pool
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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__parameter-connection:

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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__parameter-connection/base_url:

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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__parameter-connection/login_path:

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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__parameter-connection/password:

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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__parameter-connection/timeout:

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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__parameter-connection/username:

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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__parameter-connection/validate_certs:

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
        <div class="ansibleOptionAnchor" id="parameter-critical_threshold"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__parameter-critical_threshold:

      .. rst-class:: ansible-option-title

      **critical_threshold**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-critical_threshold" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Pool usage threshold in % (from 1 to 99) for sending alerts with level Critical.

      Used only with \ :emphasis:`provision`\  == \ :literal:`thick`\ 


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-drive_group"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__parameter-drive_group:

      .. rst-class:: ansible-option-title

      **drive_group**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-drive_group" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Name of the drive group


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-drives_count"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__parameter-drives_count:

      .. rst-class:: ansible-option-title

      **drives_count**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-drives_count" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Pool size in disks

      One of the following arguments is required, when new pool is creating - \ :literal:`size`\ , \ :literal:`device\_count`\ 

      Mutually exclusive with \ :literal:`size`\ 


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-name"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__parameter-name:

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

      Name of the pool


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-protection"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__parameter-protection:

      .. rst-class:: ansible-option-title

      **protection**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-protection" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Data protection scheme

      Required when new pool is creating


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`1+1`
      - :ansible-option-choices-entry:`2+1`
      - :ansible-option-choices-entry:`2+2`
      - :ansible-option-choices-entry:`4+1`
      - :ansible-option-choices-entry:`4+2`
      - :ansible-option-choices-entry:`4+3`
      - :ansible-option-choices-entry:`4+4`
      - :ansible-option-choices-entry:`8+1`
      - :ansible-option-choices-entry:`8+2`
      - :ansible-option-choices-entry:`8+3`
      - :ansible-option-choices-entry:`8+4`
      - :ansible-option-choices-entry:`8+5`
      - :ansible-option-choices-entry:`8+6`
      - :ansible-option-choices-entry:`8+7`
      - :ansible-option-choices-entry:`8+8`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-provision"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__parameter-provision:

      .. rst-class:: ansible-option-title

      **provision**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-provision" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Type of resources reservation

      Required if new pool is creating


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`thin`
      - :ansible-option-choices-entry:`thick`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-size"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__parameter-size:

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

      Pool volume

      One of the following arguments is required, when new pool is creating - \ :literal:`size`\ , \ :literal:`device\_count`\ 

      Mutually exclusive with \ :literal:`device\_count`\ 

      Can be presented as a string number with postfix. For example '100 MiB'. Following postfixes are allowed - [B, KB, MB, GB, TB, PB, EB, ZB, YB, KiB, MiB, GiB, TiB, PiB, EiB, ZiB, YiB]

      If no postfix is passed, 'B' (bytes) will be used.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-spare_count"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__parameter-spare_count:

      .. rst-class:: ansible-option-title

      **spare_count**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-spare_count" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Count of reserved drives


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__parameter-state:

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

      \ :literal:`present`\  create new pool or change existing

      With existing pool it is allowed only resizing (\ :emphasis:`size`\  or \ :emphasis:`drives\_count`\ ) and changing \ :emphasis:`spare\_count`\  and thresholds

      \ :literal:`absent`\  removes existing pool. Only pool without resources can be removed


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`present` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`absent`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-stripe_size"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__parameter-stripe_size:

      .. rst-class:: ansible-option-title

      **stripe_size**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-stripe_size" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Size of stripe


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-wait_timeout"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__parameter-wait_timeout:

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

      The number of seconds for waiting until pool will be ready


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`60`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-warning_threshold"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__parameter-warning_threshold:

      .. rst-class:: ansible-option-title

      **warning_threshold**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-warning_threshold" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Pool usage threshold in % (from 1 to 99) for sending alerts with level Warning.

      Used only with \ :emphasis:`provision`\  == \ :literal:`thin`\ 


      .. raw:: html

        </div>


.. Attributes


.. Notes

Notes
-----

.. note::
   - Fact pool size may differ from \ :literal:`size`\  value. Real size will be returned by module
   - Pool removing takes some time in Tatlin. It means that after execution module with state \ :literal:`absent`\  task completes, but pool can still exist. Therefore, if new pool is created after removing pool with same name, it needs to be ensure that pool doesn't exists. This operation is out of scope of this module. \ :ref:`yadro.tatlin.tatlin\_sp\_pools\_info <ansible_collections.yadro.tatlin.tatlin_sp_pools_info_module>`\  can be used in that case

.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Create new pool
      yadro.tatlin.tatlin_sp_pool:
        connection: "{{ connection }}"
        drive_group: HDD_209.71MB
        name: testpool
        protection: '1+1'
        provision: 'thin'
        size: 192 MiB
        spare_count: 1
        stripe_size: 4KiB
        warning_threshold: 80
        critical_threshold: 95

    - name: Resize pool
      yadro.tatlin.tatlin_sp_pool:
        connection: "{{ connection }}"
        drive_group: HDD_209.71MB
        name: testpool
        drives_count: 5

    - name: Update thresholds
      yadro.tatlin.tatlin_sp_pool:
        connection: "{{ connection }}"
        drive_group: HDD_209.71MB
        name: testpool
        warning_threshold: 75
        critical_threshold: 90

    - name: Remove pool
      yadro.tatlin.tatlin_sp_pool:
        connection: "{{ connection }}"
        drive_group: HDD_209.71MB
        name: testpool
        state: absent




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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__return-error:

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

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__return-msg:

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
        <div class="ansibleOptionAnchor" id="return-real_size"></div>

      .. _ansible_collections.yadro.tatlin.tatlin_sp_pool_module__return-real_size:

      .. rst-class:: ansible-option-title

      **real_size**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-real_size" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Real pool size (may be defferent from \ :emphasis:`size`\ )

      Always None if \ :emphasis:`state`\  is \ :literal:`absent`\ 


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` on success


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

