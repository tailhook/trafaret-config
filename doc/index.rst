.. Trafaret Config documentation master file, created by
   sphinx-quickstart on Thu Aug  4 09:16:52 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Trafaret Config's documentation!
===========================================

Trafaret-config is a wrapper that loads yaml and checks config using trafaret_
while keeping track of actual lines of file where error has happened.

Additionally, it can pretty print the error.


Contents
--------

.. toctree::
   :maxdepth: 2

   simple_api
   error
   commandline


Basic Usage
-----------

For easier real-life usage see `Command-Line`_ section.

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

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

