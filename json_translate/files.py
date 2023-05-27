# -*- coding: utf-8 -*-
import os
import re
import json


def get_input_dir_from_file(file):
    return os.path.normpath(file)


def get_json_file_name_from_input_file(input_file: str) -> str:
    return os.path.basename(input_file).split(".")[0]


def find_files(path: str) -> list:
    """
    Find all json files in folder

    :param path: directory path to list files
    :return: files in directory
    """
    return [file for file in os.listdir(path) if re.search(r"\.json$", file)]


def get_input_file(json_files: list, input_dir: str) -> str:
    """
    Get input file from folder

    :param json_files: list of files in directory
    :param input_dir: directory containing these files
    :return: file to translate
    """
    if len(json_files) == 0:
        print("No files found")
        exit(1)

    if len(json_files) == 1:
        return json_files[0]

    if len(json_files) > 1:
        print("Choose the file to use as source file:")
        for idx, file in enumerate(json_files):
            print(f"[{idx}] {file}")

        file_idx = input("Type file number: ")
        return os.path.join(input_dir, json_files[int(file_idx)])


def get_input_file_from_dir(input_dir: str):
    """
    Get input file from dir

    :param input_dir: selected folder to search for files
    :return: file to translate
    """
    if os.path.isdir(input_dir):
        json_files = find_files(input_dir)
        return get_input_file(json_files, input_dir)

    if not input_dir.endswith(".json"):
        print("You must select a json file or a folder containing json files")
        exit(1)

    if not os.path.isfile(os.path.normpath(input_dir)):
        print("File not found")
        exit(1)

    return os.path.normpath(input_dir)


def get_output_file(output: str, lang_code: str, input_file: str) -> str:
    """
    Get output file

    :param output: output file
    :param lang_code: output file language code
    :param input_file: input file
    :return: file to output translations
    """
    output_file_name = output if output else f"{lang_code}.json"

    if not output_file_name.endswith(".json"):
        output_file_name += ".json"

    output_file = os.path.join(os.path.dirname(input_file), output_file_name)

    if os.path.exists(output_file):
        override = input(
            f"File {output_file_name} already exists."
            " Do you want to override it? [Y/n] "
        )
        if not override.lower() in ("y", "yes", "ok", ""):
            output_file_name = input(f"Enter the new file name: ")
            if not output_file_name.endswith(".json"):
                output_file_name += ".json"

            return os.path.join(os.path.dirname(input_file), output_file_name)
    return output_file


def save_results_file(
    data: dict,
    output_file: str,
    indent: int = 2,
    encoding: str = "utf8",
) -> None:
    """
    Write output file

    :param data: dict object to dump into file
    :param output_file: output file path
    :param indent: json indentation
    :param encoding: file encoding
    """
    with open(output_file, "w", encoding=encoding) as file:
        json.dump(data, file, indent=indent, ensure_ascii=False)

    print(f"Results saved on {output_file}")
