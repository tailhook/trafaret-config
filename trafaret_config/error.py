import sys
from collections import namedtuple
from collections import defaultdict
import trafaret


MAX = float('inf')
try:
    SCALAR_TYPES = (str, unicode, int, float)
except NameError:
    SCALAR_TYPES = (str, int, float)


class ErrorLine(object):
    __slots__ = ('start_mark', 'end_mark', 'path', 'message', 'value')

    def __init__(self, marks, path, message, value=None):
        if marks:
            self.start_mark, self.end_mark = marks
        else:
            self.start_mark = None
            self.end_mark = None
        self.path = path
        self.message = message
        self.value = value

    def __str__(self):
        if self.start_mark:
            if self.path:
                return '{}:{}: {}: {}'.format(
                    self.start_mark.name, self.start_mark.line+1,
                    self.path, self.message)
            else:
                return '{}:{}: {}'.format(
                    self.start_mark.name, self.start_mark.line+1,
                    self.message)
        else:
            if self.path:
                return '{}: {}'.format(self.path, self.message)
            else:
                return 'CONFIG ERROR: {}'.format(self.message)

    def hint(self):
        value = self.value
        if value is None:
            return
        if isinstance(value, SCALAR_TYPES):
            return [repr(value).lstrip('u')]
        if hasattr(value, '_trafaret_config_hint'):
            return value._trafaret_config_hint()


def _is_simple_or(traf, data):
    """Simple or is when all subtrafarets are dicts and they are distinguished
    by a single key which is atom and all it's atom values are distinct
    """
    intersect = None
    dic = defaultdict(list)
    for child in traf.trafarets:
        if not isinstance(child, trafaret.Dict):
            return None, None, None
        if intersect is None:
            intersect = set(key.name for key in child.keys)
        else:
            intersect.intersection_update(key.name for key in child.keys)
        for key in child.keys:
            if key.name in intersect:
                dic[key.name].append(key.trafaret)
        if not intersect:
            return None, None, None
    key = next(iter(intersect))
    num_alters = len(traf.trafarets)
    for key in intersect:
        if not key in data:
            # this might somehow be tweaked to shorten alternatives too
            continue
        all_atoms = all(isinstance(t, trafaret.Atom) for t in dic[key])
        if all_atoms:
            values = [t.value for t in dic[key]]
            if len(set(values)) == num_alters:
                return key, data[key], values.index(data[key])
    return None, None, None

def _convert(parent_marks, prefix, err, data):
    cur_trafaret = getattr(err, 'trafaret', None)
    is_alter = isinstance(cur_trafaret, trafaret.Or)
    if is_alter:
        key, value, index = _is_simple_or(cur_trafaret, data)
        if key:
            suberror = err.error[index]
            for e in _convert(parent_marks, prefix, suberror, data.get(key)):
                yield ErrorLine([e.start_mark, e.end_mark], e.path,
                    '{} (where .{} is {!r})'.format(e.message, key, value))
            return
    if isinstance(err.error, dict):
        items = err.error.items()
    else:
        items = [('', err)]
    for key, suberror in items:
        if is_alter:
            kprefix = prefix + '.<alternative {}>'.format(key+1)
        elif isinstance(key, int):
            kprefix = prefix + '[{}]'.format(key)
        elif prefix:
            kprefix = prefix + '.' + str(key)
        else:
            kprefix = str(key)
        cmarks = getattr(data, 'marks', {})
        marks = (cmarks.get(key) or cmarks.get(str(key)) or
                 cmarks.get('__self__') or parent_marks)
        if isinstance(getattr(suberror, 'error', None), dict):
            if not is_alter and isinstance(data, dict):
                cur_data = data.get(key)
            else:
                cur_data = data
            for e in _convert(marks, kprefix, suberror, cur_data):
                yield e
        else:
            if isinstance(data, dict):
                hint = getattr(data, 'extra', {}).get(str(key),
                        data.get(str(key)))
            else:
                hint = None
            yield ErrorLine(marks, kprefix, suberror, hint)


def _err_sort_key(err):
    mark = err.start_mark
    if mark:
        return mark.name, mark.line, err.path or ''
    else:
        return 'zzzzzzzzzzzzzzz', MAX, err.path or ''


class ConfigError(Exception):

    def __init__(self, list_of_errors):
        self.errors = list_of_errors
        # Show first error in a context where one line is desired
        super(ConfigError, self).__init__(self.errors[0])

    @classmethod
    def from_loader_errors(ConfigError, error_list):
        return ConfigError(list(error_list))

    @classmethod
    def from_data_error(ConfigError, err, orig_data, extra=[]):
        errs = list(_convert(None, '', err, orig_data))
        errs.extend(extra)
        errs.sort(key=_err_sort_key)
        return ConfigError(errs)

    @classmethod
    def from_scanner_error(ConfigError, err, filename, extra=[]):
        return ConfigError([
            ErrorLine([err.problem_mark, err.problem_mark], None, err.problem),
            ErrorLine([err.problem_mark, err.problem_mark], None, err.context),
            ] + extra)

    def output(self, stream=None):
        if stream is None:
            stream = sys.stderr
        for err in self.errors:
            stream.write(str(err) + u'\n')
            hint = err.hint()
            for line in hint or ():
                stream.write(u'  -> ' + line + u'\n')
