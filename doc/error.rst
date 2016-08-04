=========
Error API
=========

.. py:class:: ConfigError

   Error returned from configuration validator. Contains filenames,
   line numbers, error messages and other info needed to pretty-print error
   messages.

   We don't provide programmatic API to access the data yet, because we're not
   sure about the details yet.

   .. py:method:: output(stream=None)

      Output the error to a stream.

      :param stream: A text stream (a file open in text mode) to write output
        to. If not specified error is printed to ``sys.stderr``. You can use
        :class:`io.StringIO` to collect output to an in-memory buffer.

      Example:

      .. code-block:: python

         try:
             config = read_and_validate(filename, trafaret)
         except ConfigError as err:
             err.output(stream=sys.stderr)
