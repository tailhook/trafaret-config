import unittest
from io import StringIO
from textwrap import dedent

import trafaret as T
from trafaret_config import parse_and_validate, ConfigError



def get_err(trafaret, text):
    data = dedent(text)
    try:
        config = parse_and_validate(text, trafaret, filename='config.yaml')
    except ConfigError as e:
        buf = StringIO()
        e.output(buf)
        return buf.getvalue()


class TestSMTP(unittest.TestCase):

    TRAFARET = T.Dict({
        T.Key('port'): T.Int(),
        T.Key('smtp'): T.Dict({
            'server': T.String(),
            'port': T.Int(),
            'ssl_port': T.Int(),
        }),
    })

    def test_bad(self):
        self.assertEqual(get_err(self.TRAFARET, """
            smtp:
                server: mail.example.org
                port: unknown
                ssl_port: NaN
            port: ???
        """),dedent("""\
            config.yaml:3: smtp.port: value can't be converted to int
            config.yaml:4: smtp.ssl_port: value can't be converted to int
            config.yaml:5: port: value can't be converted to int
        """))


class TestList(unittest.TestCase):

    TRAFARET = T.Dict({
        "hosts": T.List(T.String(regex="\w+:\d+")),
    })

    def test_ok(self):
        self.assertEqual(get_err(self.TRAFARET, """\
            hosts:
            - bear:8080
            - cat:7070
            """), None)

    def test_err(self):
        self.assertEqual(get_err(self.TRAFARET, """\
                hosts:
                - bear:8080
                - cat:x
            """),
                 "config.yaml:2: hosts[1]: "
                 "value does not match pattern: '\\\\w+:\\\\d+'\n"
            )

