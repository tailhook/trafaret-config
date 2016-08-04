import sys
import pprint
import argparse
import trafaret as T
from trafaret_config import read_and_validate, ConfigError
from trafaret_config import commandline

TRAFARET = T.Dict({
    T.Key('port', default=8080): T.Int(),
    T.Key('smtp'): T.Dict({
        'server': T.String(),
        'port': T.Int(),
        'ssl_port': T.Int(),
    }),
})


def main():
    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(ap, default_config='config.yaml')
    options = ap.parse_args()
    config = commandline.config_from_options(options, TRAFARET)
    pprint.pprint(config)

if __name__ == '__main__':
    main()
