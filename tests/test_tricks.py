import unittest
from collections import OrderedDict
from textwrap import dedent

import trafaret as T

from .util import get_err


class TestCall(unittest.TestCase):

    TRAFARET = T.Dict({
        T.Key("call_dict", optional=True):
            # The following is the ordered dict because we want to obey order
            # in the error messages. Otherwise, it could be normal dict as well
            T.Call(lambda _: T.DataError({
                "anything": "bad idea",
                "bad": "another bad idea",
            })),
        T.Key("call_str", optional=True):
            T.Call(lambda _: T.DataError("some error")),
    })

    def test_call_dict(self):
        self.assertEqual(get_err(self.TRAFARET, u"""
            call_dict: "hello"
        """), dedent(u"""\
            config.yaml:2: call_dict.anything: bad idea
            config.yaml:2: call_dict.bad: another bad idea
        """))

    def test_call_str(self):
        self.assertEqual(get_err(self.TRAFARET, u"""
            call_str: "hello"
        """), dedent(u"""\
            config.yaml:2: call_str: some error
              -> 'hello'
        """))


class TestForward(unittest.TestCase):

    FWD = T.Forward()
    TRAFARET = T.Dict({
        T.Key("value", optional=True): FWD,
    })
    FWD << T.Int()

    def test_int(self):
        self.assertEqual(get_err(self.TRAFARET, u"""
            value: "hello"
        """), dedent(u"""\
            config.yaml:2: value: value can't be converted to int
              -> 'hello'
        """))
