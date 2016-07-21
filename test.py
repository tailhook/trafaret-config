import sys
import trafaret as T
from trafaret_config import read_and_validate, ConfigError

TRAFARET = T.Dict({
    T.Key('port'): T.Int(),
    T.Key('smtp'): T.Dict({
        'server': T.String(),
        'port': T.Int(),
        'ssl_port': T.Int(),
    }),
})

try:
    config = read_and_validate('bad.yaml', TRAFARET)
except ConfigError as e:
    e.print()
    sys.exit(1)

