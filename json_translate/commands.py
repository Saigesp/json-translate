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
from translators import get_translator


def main():
    """Execute translator command."""
    parser = get_parser()
    args = parser.parse_args()

    input_dir = get_input_dir_from_file(args.file)
    input_file = get_input_file_from_dir(input_dir)
    lang_code = get_target_lang_code(args.service, args.locale)
    json_file_name = get_file_name_without_extension(input_file)

    if lang_code.lower() == json_file_name.lower():
        print("You are trying to translate to the same language!")  # noqa: T201
        exit(1)

    output_file = get_output_file(
        output=args.output,
        lang_code=lang_code,
        input_file=input_file,
        extend=args.extend,
        override=args.override,
    )
    data_to_translate = get_data_to_translate(
        input_file=input_file,
        output_file=output_file,
        extend=args.extend,
        encoding=args.encoding,
    )
    translator = get_translator(args.service)(
        target_locale=lang_code.upper(),
        source_locale=args.source_locale,
        sleep=args.sleep,
        skip=args.skip,
        encoding=args.encoding,
        log_translations=args.log,
        glossary=args.glossary,
    )
    results = translator.translate(
        data=data_to_translate,
    )
    save_results_file(
        data=results,
        output_file=output_file,
        extend=args.extend,
        indent=args.indent,
        encoding=args.encoding,
    )
