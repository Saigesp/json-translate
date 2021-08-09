#!/usr/bin/env python
import os
import re
import json
import argparse
from dotenv import load_dotenv

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

"""
Translate json files with deepl API
- Python 3 required

Usage:
    python3 main.py -d /path/to/locales-folder/
    python3 main.py -d /path/to/file.json -l en
"""

def find_files(path):
    """
    Find all json files in folder
    """
    return [file for file in os.listdir(path) if re.search(r'\.json$', file)]


def get_input_file(json_files):
    """
    Get input file from folder
    """
    if len(json_files) == 0:
        print('No files found')
        exit()

    if len(json_files) == 1:
        return json_files[0]

    if len(json_files) > 1:
        print('Choose the file to use as source file:')
        for idx, file in enumerate(json_files):
            print(f'[{idx}] {file}')

        file_idx = input('Type file number: ')
        return os.path.join(input_dir, json_files[int(file_idx)])


def get_target_lang_code(args):
    """
    Get language code from input
    """
    lang_code = '' if not args.l else args.l
    while len(lang_code) != 2:
        lang_code = input('Language code to translate to (2 letters): ')

    return lang_code.upper()


def get_strings_from_file(filepath, locale_target):
    with open(filepath) as f:
        data = json.load(f)
        return json_iterator(data, locale_target)


def json_iterator(data, locale_target, stored = {}):
    """
    Iterate over json file
    - These json files only contains dicts and strings, not arrays, booleans or numbers
    """
    for key, value in data.items():
        if type(value) == type(dict()):
            stored[key] = {}
            stored[key] = json_iterator(value, locale_target, stored[key])
        elif type(value) == type(str()):
            stored[key] = translate_string(value, locale_target)
    
    return stored


def translate_string(string, locale_target):
    if type(string) != type(str()):
        return string
    if string == '':
        return string

    return f"{string} in {locale_target}"


if __name__ == "__main__":
    load_dotenv(dotenv_path=os.path.join(CURRENT_DIR, '.env'))
    if not os.environ.get('DEEPL_AUTH_KEY'):
        raise Exception('Environment variables not loaded')

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", help="Folder to look for translation files")
    parser.add_argument("-l", help="Language target to translate")
    args = parser.parse_args()

    input_dir = os.path.normpath(args.d) if args.d else os.getcwd()

    if os.path.isdir(input_dir):
        json_files = find_files(input_dir)
        input_file = get_input_file(json_files)
    else:
        if not input_dir.endswith('.json'):
            print('You must select a json file or a folder containing json files')
            exit()
        if not os.path.isfile(os.path.normpath(input_dir)):
            print('File not found')
            exit()
        input_file = os.path.normpath(input_dir)

    lang_code = get_target_lang_code(args)
    json_file_name = input_file.split('/')[-1].split('.')[0]

    if lang_code.lower() == json_file_name.lower():
        print('You are trying to translate the same language!')
        exit()

    result = get_strings_from_file(input_file, lang_code)
    print('--> result', result)