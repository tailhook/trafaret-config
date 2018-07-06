import os
import re
from weakref import WeakKeyDictionary

from io import StringIO
import trafaret as _trafaret
from yaml import load, dump, ScalarNode
from yaml.scanner import ScannerError
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

from .error import ConfigError, ErrorLine


VARS_REGEX = re.compile(r'\$(\w+)|\{([^}]+)\}')


class ConfigDict(dict):
    __slots__ = ('marks', 'extra')

    def __init__(self, data, marks, extra):
        dict.__init__(self, data)
        self.marks = marks
        self.extra = extra


class ConfigList(list):
    __slots__ = ('marks', 'extra')

    def __init__(self, data, marks, extra):
        list.__init__(self, data)
        self.marks = marks
        self.extra = extra


class SubstInfo(object):

    def __init__(self, original, vars):
        self.original = original
        self.vars = vars

    def _trafaret_config_hint(self):
        return (
            [repr(self.original)] +
            [_format_var(k, v) for k, v in self.vars.items()]
        )


def _format_var(key, value):
    if value is None:
        return 'variable {} is undefined'.format(key)
    else:
        if value.isdecimal():
            kind = 'numeric'
        elif value.isalnum():
            if all(c.isdecimal() or 97 <= ord(c) <= 102
                   for c in value.lower()):
                kind = 'hexadecimal'
            elif value.isalpha():
                kind = 'letter'
            else:
                kind = 'alphanumeric'
        else:
            kind = 'various'
        return 'variable {!r} is {} {} characters'.format(
            key, len(value), kind)


class ConfigLoader(SafeLoader):

    def __init__(self, stream, expand_vars, errors):
        SafeLoader.__init__(self, stream)
        self.__vars = expand_vars
        self.__errors = errors

    def construct_yaml_map(self, node):
        data = ConfigDict({}, {}, {})
        yield data
        data.update(self.construct_mapping(node))
        marks = {'__self__': [node.start_mark, node.end_mark]}
        for (key, value) in node.value:
            if isinstance(key, ScalarNode):
                key_str = self.construct_scalar(key)
                marks[key_str] = cur_marks = [key.start_mark, value.end_mark]
                if(self.__expand_vars is not None and
                       isinstance(value, ScalarNode)):
                    val = data[key_str]
                    if isinstance(val, str):
                        data[key_str], ext = self.__expand_vars(val, cur_marks)
                        data.extra[key_str] = ext
        data.marks = marks

    def construct_yaml_seq(self, node):
        data = ConfigList([], {}, {})
        yield data
        data.extend(self.construct_sequence(node))
        marks = {'__self__': [node.start_mark, node.end_mark]}
        for idx, value in enumerate(node.value):
            marks[idx] = cur_marks = [value.start_mark, value.end_mark]
            if(self.__expand_vars is not None and
                   isinstance(value, ScalarNode)):
                val = data[idx]
                if isinstance(val, str):
                    data[idx], ext = self.__expand_vars(val, cur_marks)
                    data.extra[idx] = ext
        data.marks = marks

    def __expand_vars(self, value, marks):
        replaced = {}
        def replacer(match):
            key = match.group(1)
            if not key:
                key = match.group(2)
            replaced[key] = self.__vars.get(key)
            try:
                return self.__vars[key]
            except KeyError:
                self.__errors.append(ErrorLine(
                    marks, None, 'variable {!r} not found'.format(key),
                    value))
                return match.group(0)
        return VARS_REGEX.sub(replacer, value), SubstInfo(value, replaced)


ConfigLoader.add_constructor(
        'tag:yaml.org,2002:map',
        ConfigLoader.construct_yaml_map)

ConfigLoader.add_constructor(
        'tag:yaml.org,2002:seq',
        ConfigLoader.construct_yaml_seq)

def read_and_validate(filename, trafaret, vars=os.environ):
    with open(filename) as input:
        return _validate_input(input, trafaret, filename=filename, vars=vars)


def parse_and_validate(string, trafaret,
        filename='<config.yaml>', vars=os.environ):
    errors = []
    input = StringIO(string)
    input.name = filename
    return _validate_input(input, trafaret, filename=filename, vars=vars)


def _validate_input(input, trafaret, filename, vars):
    errors = []
    loader = ConfigLoader(input, vars, errors)
    try:
        data = loader.get_single_data()
    except ScannerError as e:
        raise ConfigError.from_scanner_error(e, filename, errors)
    finally:
        loader.dispose()

    try:
        result = trafaret.check(data)
    except _trafaret.DataError as e:
        raise ConfigError.from_data_error(e, data, errors)

    if errors:
        raise ConfigError.from_loader_errors(errors)
