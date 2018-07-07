import unittest
from textwrap import dedent

import trafaret as T

from .util import get_err, get_ok


class TestSubst(unittest.TestCase):

    TRAFARET = T.Dict({
        T.Key("a_int", optional=True): T.Int,
        T.Key("a_str", optional=True): T.String(),
    })

    def test_int(self):
        self.assertEqual(get_ok(self.TRAFARET, u"""
            a_int: ${NUMBER}
        """, {'NUMBER': '177'}), {'a_int': 177})

    def test_int_concat(self):
        self.assertEqual(get_ok(self.TRAFARET, u"""
            a_int: ${NUMBER}99
        """, {'NUMBER': '13'}), {'a_int': 1399})

    def test_bad_int(self):
        self.assertEqual(get_err(self.TRAFARET, u"""
            a_int: ${NUMBER}
        """, {'NUMBER': '12b'}), dedent(u"""\
            config.yaml:2: a_int: value can't be converted to int
              -> '${NUMBER}'
              -> variable 'NUMBER' consists of 3 hexadecimal characters
        """))


    def test_string(self):
        self.assertEqual(get_ok(self.TRAFARET, u"""
            a_str: http://${HOST}:$PORT/
        """, {'PORT': '8080', 'HOST': 'localhost'}), {
            'a_str': u'http://localhost:8080/',
        })

    def test_no_var(self):
        self.assertEqual(get_err(self.TRAFARET, u"""
            a_str: http://${HOST}:$PORT/
        """, {'HOST': 'localhost'}), dedent(u"""\
            config.yaml:2: variable 'PORT' not found
              -> 'http://${HOST}:$PORT/'
        """))
