import unittest
from textwrap import dedent

import trafaret as T

from .util import get_err


class TestAlternatives(unittest.TestCase):

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
