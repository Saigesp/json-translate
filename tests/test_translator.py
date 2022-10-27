# -*- coding: utf-8 -*-
import unittest
import json_translate


class Test(unittest.TestCase):
    def test_string_decode(self):
        self.assertEqual(json_translate.translator.decode_text("m\u00b2"), "m²")
