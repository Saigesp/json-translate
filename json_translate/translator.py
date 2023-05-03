# -*- coding: utf-8 -*-
import os
import json
import time
from urllib import request, parse

from settings import (
    DEEPL_API_ENDPOINT,
    GLOBAL_CACHE,
)


def translate_file(
    filepath: str,
    target_locale: str,
    sleep: float,
    skip: list = None,
) -> dict:
    """
    Get translated strings from file

    :param filepath: file path to translate
    :param target_locale: locale to translate
    :param sleep: sleep time between API calls
    :param skip: list of keys to ignore
    :return: translated file
    """
    if skip is None:
        skip = []

    with open(filepath, 'r', encoding='utf8') as f:
        data = json.load(f)
        return iterate_over_keys(
            data=data,
            target_locale=target_locale,
            sleep=sleep,
            skip=skip,
        )


def get_dict_iteration(
    data: dict, target_locale: str, sleep: float, skip: list
) -> dict:
    res = dict()
    for key, value in data.items():
        if key in skip:
            res[key] = value
        else:
            res[key] = iterate_over_keys(value, target_locale, sleep, skip)
    return res


def get_string_iteration(data: dict, target_locale: str, sleep: float) -> str:
    if data == "":
        return data
    return translate_string(data, target_locale, sleep)


def iterate_over_keys(data: dict, target_locale: str, sleep: float, skip: list):
    """
    Iterate on data and translate the corresponding values

    :param data: data to iterate
    :param target_locale: language into which the data will be translated
    :param sleep: sleep time between calls
    :param skip: list ok keys to skip (no translate)
    :return: translated block
    """
    if isinstance(data, dict):
        # Value is hierarchical, so iterate it
        return get_dict_iteration(data, target_locale, sleep, skip)

    if isinstance(data, list):
        # Value is multiple, so iterate it
        return [iterate_over_keys(value, target_locale, sleep, skip) for value in data]

    if isinstance(data, str):
        # Value is string, so translate it
        return get_string_iteration(data, target_locale, sleep)

    if isinstance(data, bool) or isinstance(data, int) or isinstance(data, float):
        # Value is boolean or numerical, return same value
        return data


def translate_string(
    text: str,
    target_locale: str,
    sleep: float,
    cache: dict = None,
) -> str:
    """
    Translate a specifig string

    Test with curl:
    $ curl https://api-free.deepl.com/v2/translate -d auth_key=YOUR-API-KEY-HERE -d "text=Hello, world!" -d "target_lang=ES"

    :param text: string to translate
    :param target_locale: language into which the data will be translated
    :param sleep: sleep time between calls
    :param cache: cache object
    :return: string translation
    """
    global GLOBAL_CACHE
    if type(text) != type(str()):
        return text

    if cache is not None:
        try:
            res = GLOBAL_CACHE[text]
            print("Using cache: ", text, " -> ", res)
            return res
        except KeyError:
            pass

    time.sleep(sleep)

    data = parse.urlencode(
        {
            "target_lang": target_locale,
            "auth_key": os.environ.get("DEEPL_AUTH_KEY"),
            "text": text,
            "preserve_formatting": "1",
        }
    ).encode()

    req = request.Request(DEEPL_API_ENDPOINT, data=data)
    response = request.urlopen(req)  # nosec

    if response.status != 200:
        print(f"{text}  ->  ERROR (response status {response.status})")
        return text

    response_data = json.loads(response.read())

    if not "translations" in response_data:
        print(f"{text}  ->  ERROR (response empty {response_data})")
        return text

    print(text, " -> ", response_data["translations"][0]["text"])

    if len(response_data["translations"]) > 1:
        print(f"({text}) More than 1 translation: {response_data['translations']}")

    dec_text = decode_text(response_data["translations"][0]["text"])
    if cache:
        cache[text] = dec_text
    return dec_text


def decode_text(text: str) -> str:
    return str(text)
