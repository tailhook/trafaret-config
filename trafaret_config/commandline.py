import sys
import yaml
import os.path

from .simple import read_and_validate
from .error import ConfigError


def standard_argparse_options(argument_parser, default_config):
    argument_parser.add_argument('-c', '--config', default=default_config,
        help="Configuration file (default: %(default)r)")
    argument_parser.add_argument('--print-config', action='store_true',
        help="Print config as it is read after parsing and exit")
    argument_parser.add_argument('-C', '--check-config', action='store_true',
        help="Check configuration and exit")


def config_from_options(options, trafaret):

    try:
        config = read_and_validate(options.config, trafaret)
    except ConfigError as e:
        e.output()
        sys.exit(1)

    if getattr(options, 'print_config'):
        yaml.dump(config, sys.stdout, default_flow_style=False)
        sys.exit(0)

    if getattr(options, 'check_config'):
        sys.exit(0)

    return config
