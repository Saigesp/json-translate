#!/usr/bin/env python
# -*- coding: utf-8 -*-
from argparser import get_parser
from languages import get_target_lang_code
from files import (
    get_input_dir_from_file,
    get_file_name_without_extension,
    get_input_file_from_dir,
    get_output_file,
    get_data_to_translate,
    save_results_file,
)
from translators.deepl import DeepLTranslator


def main():
    """Execute translator command."""
    parser = get_parser("json_translate")
    args = parser.parse_args()

    input_dir = get_input_dir_from_file(args.file)
    input_file = get_input_file_from_dir(input_dir)
    lang_code = get_target_lang_code(args.locale)
    json_file_name = get_file_name_without_extension(input_file)

    if lang_code.lower() == json_file_name.lower():
        print("You are trying to translate the same language!")  # noqa: T201
        exit(1)

    output_file = get_output_file(
        output=args.output,
        lang_code=lang_code,
        input_file=input_file,
        extend=args.extend,
    )
    data_to_translate = get_data_to_translate(
        input_file=input_file,
        output_file=output_file,
        extend=args.extend,
        encoding=args.encoding,
    )
    translator = DeepLTranslator(
        target_locale=lang_code.upper(),
        source_locale=args.source_locale,
        glossary=args.glossary,
        sleep=args.sleep,
        skip=args.skip,
        encoding=args.encoding,
        log_translations=args.log,
    )
    results = translator.translate(data=data_to_translate)
    save_results_file(
        data=results,
        output_file=output_file,
        extend=args.extend,
        indent=args.indent,
        encoding=args.encoding,
    )


if __name__ == "__main__":
    main()
