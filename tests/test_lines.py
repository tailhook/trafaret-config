import unittest
from textwrap import dedent

import trafaret as T
from .util import get_err


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
        self.assertEqual(get_err(self.TRAFARET, u"""\
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
        "hosts": T.List(T.String() & T.Regexp("\w+:\d+")),
    })

    def test_ok(self):
        self.assertEqual(get_err(self.TRAFARET, u"""\
            hosts:
            - bear:8080
            - cat:7070
            """), None)

    def test_err(self):
        self.assertEqual(get_err(self.TRAFARET, u"""\
                hosts:
                - bear:8080
                - cat:x
            """),
                 "config.yaml:3: hosts[1]: "
                 "does not match pattern \\w+:\\d+\n"
            )


class TestInvalidYaml(unittest.TestCase):

    TRAFARET = T.Dict()

    def test_star(self):
        self.assertIn(get_err(self.TRAFARET, u"""\
                port: 8080
                host: localhost
                *: 1
            """),{
            # message depends on whether we use libyaml (C speedups) or not
            dedent(  # with C speedups
                "config.yaml:3: did not find expected alphabetic or "
                    "numeric character\n"
                "config.yaml:3: while scanning an alias\n"
            ), dedent(  # without C speedups
                "config.yaml:3: expected alphabetic or numeric character, "
                    "but found ':'\n"
                "config.yaml:3: while scanning an alias\n"
            )})
