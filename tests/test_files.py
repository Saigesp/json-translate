# -*- coding: utf-8 -*-
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from json_translate import files


class FilesTest(unittest.TestCase):
    """Tests for files module."""

    @patch("files.get_input_file")
    def test_get_input_file_from_dir_calls_get_input_file_if_input_is_dir(self, get_input_file_mock: MagicMock):
        """It calls get_input_file when input is a folder."""
        files.get_input_file_from_dir("tests/data")
        get_input_file_mock.assert_called_once_with(['en_US.json', 'fr.json'], 'tests/data')

    def test_get_input_file_from_dir_exits_if_input_file_is_not_json(self):
        """It exists when input file is not json."""
        with self.assertRaises(SystemExit):
            files.get_input_file_from_dir("tests/test_files.py")

    def test_get_input_file_from_dir_exits_if_input_file_not_exists(self):
        """It exists when input file doesn't exit."""
        with self.assertRaises(SystemExit):
            files.get_input_file_from_dir("tests/lorem.json")

    def test_get_input_file_from_dir_returns_path(self):
        """It returns a Path instance."""
        result = files.get_input_file_from_dir("tests/data/en_US.json")
        self.assertTrue(isinstance(result, Path))

    def test_get_input_dir_from_file_removes_redundat_separators(self):
        """It normalize a pathname.

        It normalize a pathname by collapsing redundant separators and
        up-level references
        """
        self.assertEqual(files.get_input_dir_from_file("lorem//ipsum"), "lorem/ipsum")

    def test_get_input_dir_from_file_removes_uplevel_refs(self):
        """It normalize a pathname by collapsing up-level references."""
        self.assertEqual(files.get_input_dir_from_file("lorem/ipsum/"), "lorem/ipsum")

    def test_get_file_name_without_extension_returns_filename(self):
        """Test get_file_name_without_extension() returns the file name."""
        self.assertEqual(
            files.get_file_name_without_extension("lorem/ipsum-dolor.json"),
            "ipsum-dolor",
        )

    def test_get_input_file_raises_systemexit_if_not_json_files_provided(self):
        """Test get_input_file() raises system exit if not json files are provided."""
        with self.assertRaises(SystemExit):
            files.get_input_file([], "lorem/ipsum")

    def test_get_input_file_returns_unique_jsonfile_if_ony_one_file_provided(self):
        """Test get_input_file() returns unique json file if one file is provided."""
        self.assertEqual(
            files.get_input_file(["lorem.json"], "ipsum/dolor"),
            "lorem.json",
        )
