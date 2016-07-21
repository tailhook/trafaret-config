from weakref import WeakKeyDictionary

import trafaret as _trafaret
from yaml import load, dump, ScalarNode
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

from .error import ConfigError


class ConfigDict(dict):
    __slots__ = ('marks',)

    def __init__(self, data, marks):
        dict.__init__(self, data)
        self.marks = marks


class ConfigLoader(SafeLoader):

    def __init__(self, stream):
        SafeLoader.__init__(self, stream)

    def construct_yaml_map(self, node):
        data = ConfigDict({}, {})
        yield data
        data.update(self.construct_mapping(node))
        marks = {'__self__': [node.start_mark, node.end_mark]}
        for (key, value) in node.value:
            if isinstance(key, ScalarNode):
                marks[self.construct_scalar(key)] = [
                    key.start_mark, value.end_mark]
        data.marks = marks


ConfigLoader.add_constructor(
        'tag:yaml.org,2002:map',
        ConfigLoader.construct_yaml_map)


def read_and_validate(filename, trafaret):
    with open(filename) as input:
        loader = ConfigLoader(input)
        try:
            data = loader.get_single_data()
        finally:
            loader.dispose()

    try:
        return trafaret.check(data)
    except _trafaret.DataError as e:
        raise ConfigError.from_data_error(e, data)
