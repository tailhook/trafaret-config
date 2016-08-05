from weakref import WeakKeyDictionary

from io import StringIO
import trafaret as _trafaret
from yaml import load, dump, ScalarNode
from yaml.scanner import ScannerError
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


class ConfigList(list):
    __slots__ = ('marks',)

    def __init__(self, data, marks):
        list.__init__(self, data)
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

    def construct_yaml_seq(self, node):
        data = ConfigList([], {})
        yield data
        data.extend(self.construct_sequence(node))
        marks = {'__self__': [node.start_mark, node.end_mark]}
        for idx, value in enumerate(node.value):
            marks[idx] = [value.start_mark, value.end_mark]
        data.marks = marks


ConfigLoader.add_constructor(
        'tag:yaml.org,2002:map',
        ConfigLoader.construct_yaml_map)

ConfigLoader.add_constructor(
        'tag:yaml.org,2002:seq',
        ConfigLoader.construct_yaml_seq)

def read_and_validate(filename, trafaret):
    with open(filename) as input:
        loader = ConfigLoader(input)
        try:
            data = loader.get_single_data()
        except ScannerError as e:
            raise ConfigError.from_scanner_error(e, filename)
        finally:
            loader.dispose()

    try:
        return trafaret.check(data)
    except _trafaret.DataError as e:
        raise ConfigError.from_data_error(e, data)


def parse_and_validate(string, trafaret, filename='<config.yaml>'):
    input = StringIO(string)
    input.name = filename
    loader = ConfigLoader(input)
    try:
        data = loader.get_single_data()
    except ScannerError as e:
        raise ConfigError.from_scanner_error(e, filename)
    finally:
        loader.dispose()

    try:
        return trafaret.check(data)
    except _trafaret.DataError as e:
        raise ConfigError.from_data_error(e, data)
