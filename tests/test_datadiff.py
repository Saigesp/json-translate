# -*- coding: utf-8 -*-
import unittest
from json_translate.datadiff import DataDiff


class DataDiffTest(unittest.TestCase):
    """Tests for datadiff module."""

    def test_simple_dict(self):
        """Test a simple dict."""
        data1 = {"lorem": "ipsum"}
        data2 = {"lorem": "ipsum", "dolor": "sit"}
        diff = DataDiff(data1, data2)
        self.assertEqual(diff.to_dict(), {"dolor": "sit"})

    def test_nested_dict(self):
        """Test a nested dict."""
        data1 = {
            "lorem": {"ipsum": "zero"},
            "dolor": {
                "sit": "one",
            },
        }
        data2 = {
            "lorem": {"ipsum": "zero"},
            "dolor": {
                "sit": "one",
                "amet": "two",
            },
            "five": {"one": "tua"},
        }
        expected_diff = {"dolor": {"amet": "two"}, "five": {"one": "tua"}}
        diff = DataDiff(data1, data2)
        self.assertEqual(diff.to_dict(), expected_diff)

    def test_multi_nested_dict(self):
        """Test a multiple nesting levels dict."""
        data1 = {
            "common": {
                "lorem": "ipsum",
                "dolor": {"dolor-sit": "dolor-amet"},
                "numbers": ["one"],
            },
        }
        data2 = {
            "common": {
                "lorem": "ipsum",
                "dolor": {"dolor-sit": "dolor-amet"},
                "numbers": ["one", "two"],
                "consectur": "adisciplinit",
            },
            "main": "noodle",
        }
        expected_diff = {
            "common": {
                "numbers": ["one", "two"],
                "consectur": "adisciplinit",
            },
            "main": "noodle",
        }
        diff = DataDiff(data1, data2)
        self.assertEqual(diff.to_dict(), expected_diff)
