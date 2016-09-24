Command-Line
============

Usually you want to accept filename of a configuration file from the
command-line. While it's easy to define command-line arguments yourself,
there are two helpers, which allow to define options with the standard
names, so all of your applications are configured in the same way.

Usage:

.. code-block:: python

    from trafaret_config import read_and_validate, ConfigError
    from trafaret_config import commandline
    from your_config_module import CONFIG_TRAFARET

    def main():
        ap = argparse.ArgumentParser()
        commandline.standard_argparse_options(ap, default_config='config.yaml')
        #
        # define your command-line arguments here
        #
        options = ap.parse_args()
        config = commandline.config_from_options(options, CONFIG_TRAFARET)
        pprint.pprint(config)


You can find `full example`_ in the repository.

.. _full example: https://github.com/tailhook/trafaret_config/blob/master/example.py
