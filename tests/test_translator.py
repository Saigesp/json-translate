# -*- coding: utf-8 -*-
import unittest
import json_translate


class TranslatorTest(unittest.TestCase):
    def test_string_decode(self):
        self.assertEqual(json_translate.translator.decode_text("m\u00b2"), "m²")
