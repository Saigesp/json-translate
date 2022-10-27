# -*- coding: utf-8 -*-
import unittest

from main import decode_text


class Test(unittest.TestCase):
    def test_string_decode(self):
        self.assertEqual(decode_text("m\u00b2"), "m²")
