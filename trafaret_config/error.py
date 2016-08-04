import sys


MAX = float('inf')


class unknown_mark(object):
    name = '?'
    line = '?'


class ErrorLine(object):
    __slots__ = ('start_mark', 'end_mark', 'path', 'message')

    def __init__(self, marks, path, message):
        if marks:
            self.start_mark, self.end_mark = marks
        else:
            self.start_mark, self.end_mark = unknown_mark, unknown_mark
        self.path = path
        self.message = message

    def __str__(self):
        return '{}:{}: {}: {}'.format(
            self.start_mark.name, self.start_mark.line,
            self.path, self.message)


def _convert(parent_marks, prefix, err, data):
    for key, suberror in err.error.items():
        if isinstance(key, int):
            kprefix = prefix + '[{}]'.format(key)
        elif prefix:
            kprefix = prefix + '.' + str(key)
        else:
            kprefix = str(key)
        marks = data.marks.get(key)
        if isinstance(suberror.error, dict):
            for e in _convert(marks, kprefix, suberror, data.get(key)):
                yield e
        else:
            yield ErrorLine(
                marks or data.marks.get('__self__') or parent_marks,
                kprefix, suberror)

def _mark_sort_key(err):
    mark = err.start_mark
    return (mark.name, mark.line if mark is not unknown_mark else MAX)


class ConfigError(Exception):

    def __init__(self, list_of_errors):
        self.errors = list_of_errors
        # Show first error in a context where one line is desired
        super().__init__(self.errors[0])

    @classmethod
    def from_data_error(ConfigError, err, orig_data):
        errs = list(_convert(None, '', err, orig_data))
        errs.sort(key=_mark_sort_key)
        return ConfigError(errs)

    def output(self, stream=None):
        if stream is None:
            stream = sys.stderr
        for err in self.errors:
            stream.write(str(err) + '\n')
