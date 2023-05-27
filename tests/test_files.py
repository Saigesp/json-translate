# -*- coding: utf-8 -*-
import unittest
from json_translate import files


class FilesTest(unittest.TestCase):
    def test_get_input_dir_from_file_removes_redundat_separators(self):
        """
        It normalize a pathname by collapsing redundant
        separators and up-level references
        """
        self.assertEqual(files.get_input_dir_from_file("lorem//ipsum"), "lorem/ipsum")

    def test_get_input_dir_from_file_removes_uplevel_refs(self):
        """
        It normalize a pathname by collapsing up-level references
        """
        self.assertEqual(files.get_input_dir_from_file("lorem/ipsum/"), "lorem/ipsum")

    def test_get_json_file_name_from_input_file_returns_filename(self):
        self.assertEqual(
            files.get_json_file_name_from_input_file("lorem/ipsum-dolor.json"),
            "ipsum-dolor",
        )

    def test_get_input_file_raises_systemexit_if_not_json_files_provided(self):
        with self.assertRaises(SystemExit):
            files.get_input_file([], "lorem/ipsum")

    def test_get_input_file_returns_unique_jsonfile_if_ony_one_file_provided(self):
        self.assertEqual(
            files.get_input_file(["lorem.json"], "ipsum/dolor"),
            "lorem.json",
        )
