# -*- coding: utf-8 -*-
import os
from pathlib import Path
import re
import json


def get_input_dir_from_file(file: os.PathLike) -> os.PathLike:
    """Get file folder."""
    return os.path.normpath(file)


def get_file_name_without_extension(input_file: os.PathLike) -> str:
    """Get file name without extension."""
    names = Path(input_file).name.split(".")
    return ".".join(names[:-1])


def find_files(path: str) -> list:
    """Find all json files in folder.

    :param path: directory path to list files
    :return: files in directory
    """
    return [file for file in os.listdir(path) if re.search(r"\.json$", file)]


def get_input_file(json_files: list, input_dir: os.PathLike) -> str:
    """Get input file from folder.

    :param json_files: list of files in directory
    :param input_dir: directory containing these files
    :return: file to translate
    """
    if len(json_files) == 0:
        print("No files found")  # noqa: T201
        exit(1)

    if len(json_files) == 1:
        return json_files[0]

    print("Choose the file to use as source file:")  # noqa: T201
    for idx, file in enumerate(json_files):
        print(f"[{idx}] {file}")  # noqa: T201

    file_idx = input("Type file number: ")
    return Path(input_dir) / json_files[int(file_idx)]


def get_input_file_from_dir(input_dir: str) -> os.PathLike:
    """Get input file from dir.

    :param input_dir: selected folder to search for files
    :return: file to translate
    """
    if Path(input_dir).is_dir():
        json_files = find_files(input_dir)
        return get_input_file(json_files, input_dir)

    if not input_dir.endswith(".json"):
        print(  # noqa: T201
            "You must select a json file or a folder containing json files"
        )
        exit(1)

    if not Path(input_dir).is_file():
        print("File not found")  # noqa: T201
        exit(1)

    return os.path.normpath(input_dir)


def get_output_file(output: str, lang_code: str, input_file: str) -> str:
    """Get output file.

    :param output: output file
    :param lang_code: output file language code
    :param input_file: input file
    :return: file to output translations
    """
    output_file_name = output if output else f"{lang_code.lower()}.json"

    if not output_file_name.endswith(".json"):
        output_file_name += ".json"

    output_file = Path(input_file).parent / output_file_name

    if output_file.exists():
        override = input(
            f"File {output_file_name} already exists."
            " Do you want to override it? [Y/n] "
        )
        if override.lower() not in ("y", "yes", "ok", ""):
            output_file_name = input("Enter the new file name: ")
            if not output_file_name.endswith(".json"):
                output_file_name += ".json"

            return Path(input_file).parent / output_file_name
    return output_file


def save_results_file(
    data: dict,
    output_file: str,
    indent: int = 2,
    encoding: str = "utf8",
) -> None:
    """Write output file.

    :param data: dict object to dump into file
    :param output_file: output file path
    :param indent: json indentation
    :param encoding: file encoding
    """
    with Path.open(output_file, "w", encoding=encoding) as file:
        json.dump(data, file, indent=indent, ensure_ascii=False)

    print(f"Results saved on {output_file}")  # noqa: T201
