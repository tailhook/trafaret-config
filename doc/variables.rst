.. _variables:

Variable Substitution
=====================

Since trafaret-config 2.0 environment variables in the config are replaced
by default, this means that config like this:

.. code-block:: yaml

    url: http://${HOST}:$PORT/

Will get ``HOST`` and ``PORT`` variables insert from the environment, and if
variable does not exist, you will get the following error::

    config.yaml:2: variable 'PORT' not found
      -> 'http://${HOST}:$PORT/'

To override variables that are subsituted pass ``vars={'some': 'dict'}`` to
any of the functions:

* ``config_from_options(..., vars=custom_vars)``
* ``read_and_validate(..., vars=custom_vars)``
* ``parse_and_validate(..., vars=custom_vars)``

To turn off variable substitution at all pass ``vars=None``
