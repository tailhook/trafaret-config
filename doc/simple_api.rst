.. default-domain:: python

==========
Simple API
==========


There are just two functions:

.. py:function:: read_and_validate(filename, trafaret)

   Reads the file at ``filename`` and validates it using trafaret. Returns
   config when configuration is fine.

   Example usage:

   .. code-block:: python

        try:
            config = read_and_validate('config.yaml', TRAFARET)
        except ConfigError as e:
            e.output()
            sys.exit(1)


.. py:function:: parse_and_validate(data, trafaret, filename='<config.yaml>')

   Parses a string and validates it using trafaret. Returns
   config when configuration is fine. For having adequate filename in error
   messages you can either pass `filename` here or you can implement your
   own error printer.

   Example usage:

   .. code-block:: python

        with open("config.yaml") as f:
            text = f.read()
        try:
            config = parse_and_validate(text, TRAFARET, filename='config.yaml')
        except ConfigError as e:
            e.output()
            sys.exit(1)

