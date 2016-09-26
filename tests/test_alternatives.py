import unittest
from textwrap import dedent

import trafaret as T

from .util import get_err

BEAUTY_ERROR = hasattr(T.DataError, 'trafaret')


class TestEasyAlternatives(unittest.TestCase):
    maxDiff = 8192

    TRAFARET = T.Dict({
        "connection": T.Or(
            T.Dict({
                "kind": T.Atom("unix"),
                "path": T.String(),
            }),
            T.Dict({
                "kind": T.Atom("tcp"),
                "host": T.String(),
                "port": T.Int,
            }),
        ),
    })

    if BEAUTY_ERROR:

        def test_tcp(self):
            self.assertEqual(get_err(self.TRAFARET, u"""
                connection:
                    kind: tcp
                    host: localhost
                    port: http
            """), dedent(u"""\
                config.yaml:2: connection.port: value can't be converted to int (where .kind is 'tcp')
            """))

        def test_unix(self):
            self.assertEqual(get_err(self.TRAFARET, u"""
                connection:
                    kind: unix
                    path: /tmp/sock
                    port: http
            """), dedent(u"""\
                config.yaml:2: connection.port: port is not allowed key (where .kind is 'unix')
            """))

    else:

        def test_tcp(self):
            self.assertEqual(get_err(self.TRAFARET, u"""
                connection:
                    kind: tcp
                    host: localhost
                    port: http
            """), dedent(u"""\
                config.yaml:3: connection[0].host: host is not allowed key
                config.yaml:3: connection[0].kind: value is not exactly 'unix'
                config.yaml:3: connection[0].path: is required
                config.yaml:3: connection[0].port: port is not allowed key
                config.yaml:3: connection[1].port: value can't be converted to int
            """))

        def test_unix(self):
            self.assertEqual(get_err(self.TRAFARET, u"""
                connection:
                    kind: unix
                    path: /tmp/sock
                    port: http
            """), dedent(u"""\
                config.yaml:3: connection[0].port: port is not allowed key
                config.yaml:3: connection[1].host: is required
                config.yaml:3: connection[1].kind: value is not exactly 'tcp'
                config.yaml:3: connection[1].path: path is not allowed key
                config.yaml:3: connection[1].port: value can't be converted to int
            """))


class TestHardAlternatives(unittest.TestCase):
    maxDiff = 8192

    TRAFARET = T.Dict({
        "connection": T.Or(
            T.Dict({
                "path": T.String(),
            }),
            T.Dict({
                "host": T.String(),
                "port": T.Int,
            }),
        ),
    })

    if BEAUTY_ERROR:

        def test_tcp(self):
            self.assertEqual(get_err(self.TRAFARET, u"""
                connection:
                    host: localhost
                    port: http
            """), dedent(u"""\
                config.yaml:3: connection.<alternative 1>.host: host is not allowed key
                config.yaml:3: connection.<alternative 1>.path: is required
                config.yaml:4: connection.<alternative 1>.port: port is not allowed key
                config.yaml:4: connection.<alternative 2>.port: value can't be converted to int
            """))

        def test_unix(self):
            self.assertEqual(get_err(self.TRAFARET, u"""
                connection:
                    path: /tmp/sock
                    port: http
            """), dedent(u"""\
                config.yaml:3: connection.<alternative 2>.host: is required
                config.yaml:3: connection.<alternative 2>.path: path is not allowed key
                config.yaml:4: connection.<alternative 1>.port: port is not allowed key
                config.yaml:4: connection.<alternative 2>.port: value can't be converted to int
            """))

    else:

        def test_tcp(self):
            self.assertEqual(get_err(self.TRAFARET, u"""
                connection:
                    host: localhost
                    port: http
            """), dedent(u"""\
                config.yaml:3: connection[0].host: host is not allowed key
                config.yaml:3: connection[0].path: is required
                config.yaml:3: connection[0].port: port is not allowed key
                config.yaml:3: connection[1].port: value can't be converted to int
            """))

        def test_unix(self):
            self.assertEqual(get_err(self.TRAFARET, u"""
                connection:
                    path: /tmp/sock
                    port: http
            """), dedent(u"""\
                config.yaml:3: connection[0].port: port is not allowed key
                config.yaml:3: connection[1].host: is required
                config.yaml:3: connection[1].path: path is not allowed key
                config.yaml:3: connection[1].port: value can't be converted to int
            """))


class TestMappingOr(unittest.TestCase):

    TRAFARET = T.Mapping(T.String, T.Dict({}) | T.Dict({}))

    if BEAUTY_ERROR:

        def test_items(self):
            self.assertEqual(
                get_err(self.TRAFARET, u"""test: qwe"""),
                dedent(u"""\
                    config.yaml:1: test.value.<alternative 1>: value is not a dict
                    config.yaml:1: test.value.<alternative 2>: value is not a dict
                """))
    else:

        def test_items(self):
            self.assertEqual(
                get_err(self.TRAFARET, u"""test: qwe"""),
                dedent(u"""\
                    config.yaml:1: test.value[0]: value is not a dict
                    config.yaml:1: test.value[1]: value is not a dict
                """))
