import unittest
from textwrap import dedent

import trafaret as T

from .util import get_err


class TestList(unittest.TestCase):

    TRAFARET = T.Dict({
        T.Key("strs", optional=True): T.List(T.String()),
        T.Key("ints", optional=True): T.List(T.Int()),
    })

    def test_strings(self):
        self.assertEqual(get_err(self.TRAFARET, u"""
            strs: [1, 2]
        """), dedent(u"""\
            config.yaml:2: strs[0]: value is not a string
            config.yaml:2: strs[1]: value is not a string
        """))

    def test_ints(self):
        self.assertEqual(get_err(self.TRAFARET, u"""
            ints: ["hello", "world"]
        """), dedent(u"""\
            config.yaml:2: ints[0]: value can't be converted to int
            config.yaml:2: ints[1]: value can't be converted to int
        """))


class TestMapping(unittest.TestCase):

    TRAFARET = T.Dict({
        T.Key("items", optional=True): T.Mapping(T.String(), T.String()),
    })

    def test_items(self):
        self.assertEqual(get_err(self.TRAFARET, u"""
            items:
              a: x
              b: 1
              3: b
        """), dedent(u"""\
            config.yaml:4: items.b.value: value is not a string
            config.yaml:5: items[3].key: value is not a string
        """))


class TestTuple(unittest.TestCase):

    TRAFARET = T.Dict({
        T.Key("tuple", optional=True): T.Tuple(T.String(), T.Int()),
    })

    def test_items(self):
        self.assertEqual(get_err(self.TRAFARET, u"""
            tuple:
            - "hello"
            - "world"
        """), dedent(u"""\
            config.yaml:4: tuple[1]: value can't be converted to int
        """))
