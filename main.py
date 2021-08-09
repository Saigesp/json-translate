#!/usr/bin/env python
import os
import re
import json
import argparse

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

    return lang_code


def get_strings_from_file(filepath):
    with open(filepath) as f:
        data = json.load(f)
        json_iterator(data)


def json_iterator(data):
    for key,value in data.items():
        if type(value) == type(dict()):
            json_iterator(value)
        elif type(value) == type(list()):
            for val in value:
                if type(val) == type(str()):
                    pass
                elif type(val) == type(list()):
                    pass
                else:
                    json_iterator(val)
        else:
            print(f"{key}: {value}")


if __name__ == "__main__":
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

    # print(input_file, lang_code)
    get_strings_from_file(input_file)