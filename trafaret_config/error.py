import sys
from collections import namedtuple


MAX = float('inf')


class ErrorLine(object):
    __slots__ = ('start_mark', 'end_mark', 'path', 'message')

    def __init__(self, marks, path, message):
        if marks:
            self.start_mark, self.end_mark = marks
        else:
            self.start_mark = None
            self.end_mark = None
        self.path = path
        self.message = message

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


def _convert(parent_marks, prefix, err, data):
    for key, suberror in err.error.items():
        if isinstance(key, int):
            kprefix = prefix + '[{}]'.format(key)
        elif prefix:
            kprefix = prefix + '.' + str(key)
        else:
            kprefix = str(key)
        cmarks = getattr(data, 'marks', {})
        marks = (cmarks.get(key) or cmarks.get(str(key)) or
                 cmarks.get('__self__') or parent_marks)
        if isinstance(getattr(suberror, 'error', None), dict):
            for e in _convert(marks, kprefix, suberror, data.get(key)):
                yield e
        else:
            yield ErrorLine(marks, kprefix, suberror)


def _mark_sort_key(err):
    mark = err.start_mark
    if mark:
        return mark.name, mark.line
    else:
        return 'zzzzzzzzzzzzzzz', MAX


class ConfigError(Exception):

    def __init__(self, list_of_errors):
        self.errors = list_of_errors
        # Show first error in a context where one line is desired
        super(ConfigError, self).__init__(self.errors[0])

    @classmethod
    def from_data_error(ConfigError, err, orig_data):
        errs = list(_convert(None, '', err, orig_data))
        errs.sort(key=_mark_sort_key)
        return ConfigError(errs)

    @classmethod
    def from_scanner_error(ConfigError, err, filename):
        return ConfigError([
            ErrorLine([err.problem_mark, err.problem_mark], None, err.problem),
            ErrorLine([err.problem_mark, err.problem_mark], None, err.context),
            ])

    def output(self, stream=None):
        if stream is None:
            stream = sys.stderr
        for err in self.errors:
            stream.write(str(err) + u'\n')
