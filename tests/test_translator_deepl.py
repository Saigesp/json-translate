# -*- coding: utf-8 -*-
import unittest
from json_translate.translators.deepl import DeepLTranslator


class TranslatorTest(unittest.TestCase):
    def test_string_decode(self):
        translator = DeepLTranslator("en")
        self.assertEqual(translator.decode_text("m\u00b2"), "m²")
