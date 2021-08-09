#!/usr/bin/env python
import os
import re
import json
import time
import argparse
from urllib import request, parse
from dotenv import load_dotenv

DEEPL_API_ENDPOINT = 'https://api-free.deepl.com/v2/translate'
SLEEP_BETWEEN_API_CALLS = 0.2 # Seconds
INDENTATION_DEFAULT = 2


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


def get_output_file(output):
    """
    Get output file
    """
    output_file_name = output if output else f"{lang_code}.json"
    if not output_file_name.endswith('.json'):
        output_file_name += '.json'
    output_file = os.path.join(os.path.dirname(input_file), output_file_name)
    if os.path.exists(output_file):
        override = input(f"File {output_file_name} already exists. Do you want to override it? [Y/N] ")
        if not override.lower() in ('y', 'yes'):
            output_file_name = input(f"Enter the new file name: ")
            if not output_file_name.endswith('.json'):
                output_file_name += '.json'
            
            return os.path.join(os.path.dirname(input_file), output_file_name)
    return output_file


def get_target_lang_code(locale):
    """
    Get language code from input
    """
    lang_code = '' if not locale else locale
    while len(lang_code) != 2:
        lang_code = input('Language code to translate to (2 letters): ')

    return lang_code


def get_strings_from_file(filepath, target_locale, sleep_time):
    with open(filepath) as f:
        data = json.load(f)
        return json_iterator(data, target_locale, sleep_time)


def json_iterator(data, target_locale, sleep_time, stored = {}):
    """
    Iterate over json file
    - These json files only contains dicts and strings, not arrays, booleans or numbers
    """
    for key, value in data.items():
        if type(value) == type(dict()):
            stored[key] = {}
            stored[key] = json_iterator(value, target_locale, sleep_time, stored[key])
        elif type(value) == type(str()):
            if value == '':
                stored[key] = value
            else:
                time.sleep(sleep_time)
                stored[key] = translate_string(value, target_locale)
    
    return stored


def translate_string(text, target_locale):
    """
    test with curl:
    $ curl https://api-free.deepl.com/v2/translate -d auth_key=YOUR-API-KEY-HERE -d "text=Hello, world!" -d "target_lang=ES"
    """
    if type(text) != type(str()):
        return text

    data = parse.urlencode({
        'target_lang' : target_locale,  
        'auth_key' : os.environ.get('DEEPL_AUTH_KEY'),
        'text': text,
    }).encode()
    req = request.Request(DEEPL_API_ENDPOINT, data=data)
    response = request.urlopen(req)

    if response.status != 200:
        print(f'{text}  ->  ERROR (response status {response.status})')
        return text

    response_data = json.loads(response.read())

    if not 'translations' in response_data:
        print(f'{text}  ->  ERROR (response empty {response_data})')
        return text

    print(text, ' -> ', response_data['translations'][0]['text'])

    if len(response_data['translations']) > 1:
        print(f"({text}) More than 1 translation: {response_data['translations']}")
    
    return response_data['translations'][0]['text']


def save_results_file(data, output_file, indent):
    """
    Write output file
    """
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=indent)
    
    print(f"Results saved on {output_file}")


if __name__ == "__main__":
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

    if not os.environ.get('DEEPL_AUTH_KEY', False):
        raise Exception('Environment variables not loaded')

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Folder or file to look for translation source")
    parser.add_argument("-o", "--output", help="Output file name")
    parser.add_argument("-l", "--locale", help="Language target to translate")
    parser.add_argument("-i", "--indent", type=int, default=INDENTATION_DEFAULT, help="Indentation spaces")
    parser.add_argument("-s", "--sleep", type=float, default=SLEEP_BETWEEN_API_CALLS, help="Sleep time between API calls")
    args = parser.parse_args()

    input_dir = os.path.normpath(args.file)

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

    lang_code = get_target_lang_code(args.locale)
    json_file_name = os.path.basename(input_file).split('.')[0]

    if lang_code.lower() == json_file_name.lower():
        print('You are trying to translate the same language!')
        exit()

    output_file = get_output_file(args.output)
    results = get_strings_from_file(input_file, lang_code.upper(), args.sleep)
    save_results_file(results, output_file, args.indent)
