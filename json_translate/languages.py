# -*- coding: utf-8 -*-
from settings import SUPPORTED_LANG_CODES


def get_target_lang_code(locale: str) -> str:
    """Get language code from input.

    :param locale: locate target to use
    :return: output locale code
    """
    lang_code = locale or ""

    while len(lang_code) > 5:
        lang_code = input(
            "Language code to translate to (usually 2 letters, unless a supported region like EN-GB): "
        )

    if lang_code not in SUPPORTED_LANG_CODES:
        # TODO: Log properly
        print(  # noqa: T201
            f"Language {lang_code} is not supported.",
            "Check the supported ones in https://www.deepl.com/docs-api/translate-text",
        )
        exit(1)

    return lang_code
