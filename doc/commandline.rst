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

The ``--help`` looks like::

    usage: example.py [-h] [-c CONFIG] [--print-config] [-C]

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            Configuration file (default: 'config.yaml')
      --print-config        Print config as it is read after parsing and exit
      -C, --check-config    Check configuration and exit

.. _full example: https://github.com/tailhook/trafaret_config/blob/master/example.py

Alternatively you can put configuration parameters into it's own option group:

.. code-block:: python

    def main():
        ap = argparse.ArgumentParser()
        commandline.standard_argparse_options(
            ap.add_argument_group('configuration'),
            default_config='config.yaml')

        ap.add_argument('--verbose', action='store_true')

Output looks like::

    usage: example-cli.py [-h] [-c CONFIG] [--print-config] [-C] [--verbose]

    optional arguments:
      -h, --help            show this help message and exit
      --verbose

    configuration:
      -c CONFIG, --config CONFIG
                            Configuration file (default: 'config.yaml')
      --print-config        Print config as it is read after parsing and exit
      -C, --check-config    Check configuration and exit
