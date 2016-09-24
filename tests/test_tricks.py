import unittest
from collections import OrderedDict
from textwrap import dedent

import trafaret as T

from .util import get_err


class TestCall(unittest.TestCase):

    TRAFARET = T.Dict({
        T.Key("call", optional=True):
            # The following is the ordered dict because we want to obey order
            # in the error messages. Otherwise, it could be normal dict as well
            T.Call(lambda x: T.DataError(OrderedDict([
                ("bad", "bad idea"),
                ("anything", "another bad idea"),
            ]))),
    })

    def test_call(self):
        self.assertEqual(get_err(self.TRAFARET, u"""
            call: "hello"
        """), dedent(u"""\
            config.yaml:2: call.bad: bad idea
            config.yaml:2: call.anything: another bad idea
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
        """))
