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

Sometimes you might want to print variables used in configuration file, i.e.
to make some configuration file inter. If you're using
``trafaret_config.commandline`` you can do it using default command-line
argument::

    $ ./run.py --print-config-vars
    HOST
    PORT
