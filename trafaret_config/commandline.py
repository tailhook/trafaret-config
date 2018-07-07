import sys
import yaml
import os.path

from . import simple
from .error import ConfigError


def standard_argparse_options(argument_parser, default_config):
    argument_parser.add_argument('-c', '--config', default=default_config,
        help="Configuration file (default: %(default)r)")
    argument_parser.add_argument('--print-config', action='store_true',
        help="Print config as it is read after parsing and exit")
    argument_parser.add_argument('--print-config-vars', action='store_true',
        help="Print variables used in configuration file")
    argument_parser.add_argument('-C', '--check-config', action='store_true',
        help="Check configuration and exit")


def config_from_options(options, trafaret, vars=os.environ):

    if getattr(options, 'print_config_vars'):
        vars = simple.read_and_get_vars(options.config, trafaret, vars=vars)
        for name in vars:
            print(name)
        sys.exit(0)

    try:
        config = simple.read_and_validate(options.config, trafaret, vars=vars)
    except ConfigError as e:
        e.output()
        sys.exit(1)

    if getattr(options, 'print_config'):
        yaml.dump(config, sys.stdout, default_flow_style=False)
        sys.exit(0)

    if getattr(options, 'check_config'):
        sys.exit(0)

    return config
