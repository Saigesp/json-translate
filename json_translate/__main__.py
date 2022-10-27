#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dotenv import load_dotenv

from parser import get_parser
from languages import get_target_lang_code
from files import (
    get_input_dir_from_file,
    get_json_file_name_from_input_file,
    get_input_file_from_dir,
    get_output_file,
    save_results_file,
)
from translator import translate_file

load_dotenv()


def main():
    parser = get_parser("json_translate")
    args = parser.parse_args()

    input_dir = get_input_dir_from_file(args.file)
    input_file = get_input_file_from_dir(input_dir)
    lang_code = get_target_lang_code(args.locale)
    json_file_name = get_json_file_name_from_input_file(input_file)

    if lang_code.lower() == json_file_name.lower():
        print("You are trying to translate the same language!")
        exit(1)

    output_file = get_output_file(args.output, lang_code, input_file)
    results = translate_file(input_file, lang_code.upper(), args.sleep, args.skip)
    save_results_file(results, output_file, args.indent)


if __name__ == "__main__":
    main()
