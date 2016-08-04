import sys
import os.path

from .simple import read_and_validate
from .error import ConfigError


def standard_argparse_options(argument_parser, default_config):
    argument_parser.add_argument('-c', '--config', default=default_config,
        help="Configuration file")
    argument_parser.add_argument('-C', '--check-config',
        help="Check configuration and exit", action='store_true')


def config_from_options(options, trafaret):

    try:
        config = read_and_validate(options.config, trafaret)
    except ConfigError as e:
        e.output()
        sys.exit(1)

    if getattr(options, 'check_config'):
        sys.exit(0)

    return config
