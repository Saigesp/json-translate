#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from settings import (
    INDENTATION_DEFAULT,
    SLEEP_BETWEEN_API_CALLS,
    ENCODING,
)


def get_parser() -> argparse.ArgumentParser:
    """Construct and return the argument parser for all commands."""
    parser = argparse.ArgumentParser(
        prog="json_translate",
        description="Translate json files using the DeepL API ",
        epilog="Report issues at https://github.com/Saigesp/json-deepl-translate/issues",
    )
    parser.add_argument(
        "service",
        help="Translation service to use",
    )
    parser.add_argument(
        "file",
        help="Folder or file to look for translation source",
    )
    parser.add_argument(
        "locale",
        help="Language target to translate",
    )
    parser.add_argument(
        "-sl",
        "--source-locale",
        help="Language translating from (required for glossary)",
    )
    parser.add_argument(
        "-g",
        "--glossary",
        help="ID of glossary to use when translating",
    )
    parser.add_argument(
        "-e",
        "--extend",
        action="store_true",
        help="Extend an existing translation file",
    )
    parser.add_argument(
        "--override",
        action="store_true",
        help="Override existing translation file (don't ask)",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output file name",
    )
    parser.add_argument(
        "-i",
        "--indent",
        type=int,
        default=INDENTATION_DEFAULT,
        help="Indentation spaces",
    )
    parser.add_argument(
        "-s",
        "--sleep",
        type=float,
        default=SLEEP_BETWEEN_API_CALLS,
        help="Sleep time between API calls",
    )
    parser.add_argument(
        "--skip",
        nargs="+",
        help="Keys to skip",
    )
    parser.add_argument(
        "--encoding",
        default=ENCODING,
        help="File encoding",
    )
    parser.add_argument(
        "--log",
        action="store_true",
        help="If print translation results",
    )

    return parser
