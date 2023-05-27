# -*- coding: utf-8 -*-
import json
from abc import ABC, abstractmethod
from settings import ENCODING, SLEEP_BETWEEN_API_CALLS


class BaseTranslator(ABC):
    cached = dict()

    class status:
        SUCCESS = 0
        WARNING = 1
        ERROR = 2

    def __init__(
        self,
        target_locale: str,
        skip: list = None,
        sleep: float = SLEEP_BETWEEN_API_CALLS,
        encoding: str = ENCODING,
        log_translations: bool = False,
    ):
        """
        Initialize translator instance

        :param target_locale: locale to translate
        :param skip: list of keys to ignore
        :param sleep: sleep time between API calls
        :param encoding: encoding (utf-8, latin-1 etc)
        :param log_translations: if print translation results
        """
        self.skip_keys = skip or []
        self.target_locale = target_locale
        self.sleep = sleep
        self.encoding = encoding
        self.log_translations = log_translations

    def translate_file(self, filepath: str):
        """
        Translate file

        :param filepath: file path to translate
        :return: translation
        """
        with open(filepath, "r", encoding=self.encoding) as f:
            self.input_data = json.load(f)

        return self.iterate_over_keys(self.input_data)

    def iterate_over_keys(self, data):
        """
        Iterate on data and translate the corresponding values

        :param data: data to iterate
        :return: translated block
        """

        if isinstance(data, dict):
            # Value is hierarchical, so iterate it
            return self.get_dict_iteration(data)

        if isinstance(data, list):
            # Value is multiple, so iterate it
            return [self.iterate_over_keys(value) for value in data]

        if isinstance(data, str):
            # Value is string, so translate it
            return self.get_string_iteration(data)

        if isinstance(data, bool) or isinstance(data, int) or isinstance(data, float):
            # Value is boolean or numerical, return same value
            return data

    def get_dict_iteration(self, data: dict) -> dict:
        result = dict()
        for key, value in data.items():
            if key in self.skip_keys:
                result[key] = value
            else:
                result[key] = self.iterate_over_keys(value)
        return result

    def get_string_iteration(self, data: str) -> str:
        if data == "":
            return data
        return self.translate_string(data)

    def decode_text(self, text: str) -> str:
        return str(text)  # TODO: improve decoding

    def log_translation(
        self,
        input_text: str,
        result: str = "",
        status: int = 0,
    ) -> None:
        if not self.log_translations:
            return

        if not status == self.status.SUCCESS:
            result = f" ({result})"
            translation = input_text

        if status == self.status.WARNING:
            str_status = "WARNING: "
        elif status == self.status.ERROR:
            str_status = "ERROR: "
        else:
            str_status = ""
            translation = f"{input_text} -> {result}"
            result = ""

        print(f"{str_status}{translation}{result}")

    @abstractmethod
    def translate_string(self):
        raise NotImplementedError
