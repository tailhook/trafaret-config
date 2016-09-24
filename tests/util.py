from io import StringIO
from textwrap import dedent
from trafaret_config import parse_and_validate, ConfigError


def get_err(trafaret, text):
    data = dedent(text)
    try:
        config = parse_and_validate(text, trafaret, filename='config.yaml')
    except ConfigError as e:
        buf = StringIO()
        e.output(buf)
        return buf.getvalue()


