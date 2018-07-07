import unittest
from textwrap import dedent

import trafaret as T

from .util import get_err


class TestScalar(unittest.TestCase):

    TRAFARET = T.Dict({
        T.Key("a_null", optional=True): T.Null,
        T.Key("a_bool", optional=True): T.Bool,
        T.Key("a_float", optional=True): T.Float,
        T.Key("a_int", optional=True): T.Int,
        T.Key("a_atom_str", optional=True): T.Atom("hello"),
        T.Key("a_atom_list", optional=True): T.Atom(["x", "y"]),
        T.Key("a_enum_str", optional=True): T.Enum(["x", "y"]),
        T.Key("a_str", optional=True): T.String(max_length=12),
        T.Key("a_email", optional=True): T.Email,
        T.Key("a_url", optional=True): T.URL,
    })

    def test_null(self):
        self.assertEqual(get_err(self.TRAFARET, u"""
            a_null: "hello"
        """), dedent(u"""\
            config.yaml:2: a_null: value should be None
              -> 'hello'
        """))

    def test_bool(self):
        self.assertEqual(get_err(self.TRAFARET, u"""
            a_bool: "hello"
        """), dedent(u"""\
            config.yaml:2: a_bool: value should be True or False
              -> 'hello'
        """))

    def test_float(self):
        self.assertEqual(get_err(self.TRAFARET, u"""
            a_float: "hello"
        """), dedent(u"""\
            config.yaml:2: a_float: value can't be converted to float
              -> 'hello'
        """))

    def test_int(self):
        self.assertEqual(get_err(self.TRAFARET, u"""
            a_int: 2.57
        """), dedent(u"""\
            config.yaml:2: a_int: value is not int
              -> 2.57
        """))

    def test_atom_str(self):
        self.assertEqual(get_err(self.TRAFARET, u"""
            a_atom_str: "xxx"
        """), dedent(u"""\
            config.yaml:2: a_atom_str: value is not exactly 'hello'
              -> 'xxx'
        """))

    def test_atom_list(self):
        self.assertEqual(get_err(self.TRAFARET, u"""
            a_atom_list: "xxx"
        """), dedent(u"""\
            config.yaml:2: a_atom_list: value is not exactly '['x', 'y']'
              -> 'xxx'
        """))

    def test_enum_str(self):
        self.assertEqual(get_err(self.TRAFARET, u"""
            a_enum_str: "hello"
        """), dedent(u"""\
            config.yaml:2: a_enum_str: value doesn't match any variant
              -> 'hello'
        """))

    def test_string(self):
        self.assertEqual(get_err(self.TRAFARET, u"""
            a_str: 1
        """), dedent(u"""\
            config.yaml:2: a_str: value is not a string
              -> 1
        """))

    def test_long_string(self):
        self.assertEqual(get_err(self.TRAFARET, u"""
            a_str: "hello my good friends"
        """), dedent(u"""\
            config.yaml:2: a_str: String is longer than 12 characters
              -> 'hello my good friends'
        """))

    def test_email(self):
        self.assertEqual(get_err(self.TRAFARET, u"""
            a_email: "hello"
        """), dedent(u"""\
            config.yaml:2: a_email: value is not a valid email address
              -> 'hello'
        """))

    def test_url(self):
        self.assertEqual(get_err(self.TRAFARET, u"""
            a_url: "hello"
        """), dedent(u"""\
            config.yaml:2: a_url: value is not URL
              -> 'hello'
        """))
