# -*- coding: utf-8 -*-
import os
import re
import json
from pathlib import Path
from mergedeep import merge
from datadiff import DataDiff


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


def get_output_file(
    *,
    output: str,
    lang_code: str,
    input_file: str,
    extend: bool = False,
    override: bool = False,
) -> str:
    """Get output file.

    :param output: output file name
    :param lang_code: output file language code
    :param input_file: input file
    :param extend: if output file must be extended
    :param override: if output file must be overrided
    :return: file to output translations
    """
    output_file_name = output if output else f"{lang_code.lower()}.json"

    if not output_file_name.endswith(".json"):
        output_file_name += ".json"

    output_file = Path(input_file).parent / output_file_name

    if output_file.exists() and not extend:
        if override:
            return output_file
        ask_override = input(
            f"File {output_file_name} already exists."
            " Do you want to override it? [Y/n] "
        )
        if ask_override.lower() not in ("y", "yes", "ok", ""):
            output_file_name = input("Enter the new file name: ")
            if not output_file_name.endswith(".json"):
                output_file_name += ".json"

            return Path(input_file).parent / output_file_name

    return output_file


def get_data_to_translate(
    input_file: os.PathLike,
    *,
    output_file: os.PathLike = None,
    extend: bool = False,
    encoding: str = "utf8",
) -> dict:
    """Get data to translate.

    :param input_file: file to translate
    :param output_file: file to save
    :param extend: if output file must be extended
    :param encoding: file encoding
    """
    if extend and (output_file is None or not output_file.exists()):
        print("Existing file to extend not found")  # noqa: T201
        exit(1)

    with Path.open(input_file, "r", encoding=encoding) as file:
        input_data = json.load(file)

    if not extend:
        return input_data

    with Path.open(output_file, "r", encoding=encoding) as file:
        existing_data = json.load(file)

    diff = DataDiff(existing_data, input_data)
    return diff.to_dict()


def save_results_file(
    data: dict,
    output_file: os.PathLike,
    *,
    extend: bool = False,
    indent: int = 2,
    encoding: str = "utf8",
) -> None:
    """Write output file.

    :param data: dict object to dump into file
    :param output_file: output file path
    :param extend: if output file must be extended
    :param indent: json indentation
    :param encoding: file encoding
    """
    if extend:
        if output_file is None or not output_file.exists():
            raise Exception("Existing file to extend not found")

        with Path.open(output_file, "r", encoding=encoding) as file:
            data = merge(json.load(file), data)

    with Path.open(output_file, "w", encoding=encoding) as file:
        json.dump(data, file, indent=indent, ensure_ascii=False)

    print(f"Results saved on {output_file}")  # noqa: T201
