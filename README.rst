===============
Trafaret Config
===============


:Status: Stable
:Documentation: http://trafaret-config.readthedocs.io/


This is a wrapper that loads yaml and checks config using trafaret_ while
keeping track of actual lines of file where error has happened. Additionally,
it can pretty print the error.

Basic Usage:

.. code-block:: python

    import argparse
    import trafaret
    from trafaret_config import commandline

    TRAFARET = trafaret.Dict({'x': trafaret.String()})

    def main():
        ap = argparse.ArgumentParser()
        commandline.standard_argparse_options(ap, default_config='config.yaml')
        #
        # define your command-line arguments here
        #
        options = ap.parse_args()
        config = commandline.config_from_options(options, TRAFARET)
        pprint.pprint(config)

Example output when there is an error in config (from a `example.py` which
has better trafaret than example above)::

    bad.yaml:3: smtp.port: value can't be converted to int
      -> 'unknown'
    bad.yaml:4: smtp.ssl_port: value can't be converted to int
      -> 'NaN'
    bad.yaml:5: port: value can't be converted to int
      -> '???'

Help looks like this::

    usage: example.py [-h] [-c CONFIG] [--print-config] [--print-config-vars] [-C]

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            Configuration file (default: 'config.yaml')
      --print-config        Print config as it is read after parsing and exit
      --print-config-vars   Print variables used in configuration file
      -C, --check-config    Check configuration and exit


Since trafaret-config 2.0 environment variables in the config are replaced
by default, this means that config like this:

.. code-block:: yaml

    url: http://${HOST}:$PORT/

Will get ``HOST`` and ``PORT`` variables insert from the environment, and if
variable does not exist, you will get the following error::

    config.yaml:2: variable 'PORT' not found
      -> 'http://${HOST}:$PORT/'

Low-level interface, without relying on argparse:

.. code-block:: python

   import sys
   import trafaret
   from trafaret_config import ConfigError, read_and_validate

   TRAFARET = trafaret.Dict({'x': trafaret.String()})

   try:
       config = read_and_validate('config.yaml', TRAFARET)
   except ConfigError as e:
       e.output()
       sys.exit(1)



.. _trafaret: http://github.com/Deepwalker/trafaret

Installation
============

::

    pip install trafaret-config==2.0.0-beta.2


License
=======

Licensed under either of

* Apache License, Version 2.0,
  (./LICENSE-APACHE or http://www.apache.org/licenses/LICENSE-2.0)
* MIT license (./LICENSE-MIT or http://opensource.org/licenses/MIT)
  at your option.

------------
Contribution
------------

Unless you explicitly state otherwise, any contribution intentionally
submitted for inclusion in the work by you, as defined in the Apache-2.0
license, shall be dual licensed as above, without any additional terms or
conditions.
