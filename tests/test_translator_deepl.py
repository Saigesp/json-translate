# -*- coding: utf-8 -*-
import unittest
from json_translate.translators.deepl import DeepLTranslator


class TranslatorTest(unittest.TestCase):
    """Test DeepL translator."""

    def test_string_decode(self):
        """Test encoded string."""
        translator = DeepLTranslator("en")
        self.assertEqual(translator.decode_text("m\u00b2"), "m²")
