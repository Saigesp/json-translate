# -*- coding: utf-8 -*-
from settings import DEELP_SUPPORTED_LANGS, AWS_SUPPORTED_LANGS


def get_target_lang_code(service: str, locale: str) -> str:
    """Get language code from input.

    :param service: translation service to use
    :param locale: locate target to use
    :return: output locale code
    """
    lang_code = locale or ""

    while len(lang_code) > 5:
        lang_code = input(
            "Language code to translate to (usually 2 letters, unless a supported region like EN-GB): "
        )

    if service == "deepl" and lang_code.upper() not in DEELP_SUPPORTED_LANGS:
        # TODO: Log properly
        print(  # noqa: T201
            f"Language {lang_code} is not supported by DeepL.",
            "Check the supported ones in https://www.deepl.com/docs-api/translate-text",
        )
        exit(1)

    if service == "aws" and lang_code.lower() not in AWS_SUPPORTED_LANGS:
        # TODO: Log properly
        print(  # noqa: T201
            f"Language {lang_code} is not supported by AWS.",
            "Check the supported ones in https://docs.aws.amazon.com/translate/latest/dg/what-is-languages.html",
        )
        exit(1)

    return lang_code
