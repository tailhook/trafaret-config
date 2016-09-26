====================
Configuration Loader
====================


:Status: Beta


This is a wrapper that loads yaml and checks config using trafaret_ while
keeping track of actual lines of file where error has happened. Additionally,
it can pretty print the error.

Basic Usage:

.. code-block:: python

   import trafaret
   from trafaret_config import read_and_validate

   TRAFARET = trafaret.Dict({'x': trafaret.String()})

   try:
       config = read_and_validate('config.yaml', TRAFARET)
   except ConfigError as e:
       e.output()
       sys.exit(1)


Example output (from a `test.py` which has better trafaret than example
above)::

    bad.yaml:2: smtp.port: value can't be converted to int
    bad.yaml:3: smtp.ssl_port: value can't be converted to int
    bad.yaml:4: port: value can't be converted to int


.. _trafaret: http://github.com/Deepwalker/trafaret

Installation
============

::

    pip install trafaret-config==0.1.1


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
