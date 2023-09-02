# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from settings import ENCODING, SLEEP_BETWEEN_API_CALLS


class BaseTranslator(ABC):
    """Translator Abstract base class.

    Use this class to implement translators
    """

    cached = {}

    class Status:
        """Translation result status."""

        success: int = 0
        warning: int = 1
        error: int = 2

    def __init__(
        self,
        target_locale: str,
        source_locale: str = None,
        glossary: str = None,
        skip: list = None,
        sleep: float = SLEEP_BETWEEN_API_CALLS,
        encoding: str = ENCODING,
        log_translations: bool = False,
    ):
        """Initialize translator instance.

        :param target_locale: locale to translate
        :param skip: list of keys to ignore
        :param sleep: sleep time between API calls
        :param encoding: encoding (utf-8, latin-1 etc)
        :param log_translations: if print translation results
        """
        self.skip_keys = skip or []
        self.target_locale = target_locale
        self.source_locale = source_locale
        self.glossary = glossary
        self.sleep = sleep
        self.encoding = encoding
        self.log_translations = log_translations

    def translate(self, data: dict) -> dict:
        """Translate nested data.

        :param data: data to translate
        :return: translation
        """
        return self._iterate_over_keys(data)

    def _iterate_over_keys(self, data) -> list | dict | str:
        """Iterate on data and translate the corresponding values.

        :param data: data to iterate
        :return: translated block
        """
        if isinstance(data, dict):
            # Value is hierarchical, so iterate it
            return self._get_dict_iteration(data)

        if isinstance(data, list):
            # Value is multiple, so iterate it
            return [self._iterate_over_keys(value) for value in data]

        if isinstance(data, str):
            # Value is string, so translate it
            return self._get_string_iteration(data)

        if isinstance(data, (bool | int | float)):
            # Value is boolean or numerical, return same value
            return data

        raise Exception(f"Can't determine {data} type")

    def _get_dict_iteration(self, data: dict) -> dict:
        result = {}
        for key, value in data.items():
            if key in self.skip_keys:
                result[key] = value
            else:
                result[key] = self._iterate_over_keys(value)
        return result

    def _get_string_iteration(self, data: str) -> str:
        if data == "":
            return data
        return self.translate_string(data)

    def decode_text(self, text: str) -> str:
        """Decode text."""
        return str(text)  # TODO: improve decoding

    def log_translation(
        self,
        input_text: str,
        result: str = "",
        status: int = 0,
    ) -> None:
        """Log translations result."""
        if not self.log_translations:
            return

        if status != self.Status.success:
            result = f" ({result})"
            translation = input_text

        if status == self.Status.warning:
            str_status = "warning: "
        elif status == self.Status.error:
            str_status = "error: "
        else:
            str_status = ""
            translation = f"{input_text} -> {result}"
            result = ""

        # TODO: log properly
        print(f"{str_status}{translation}{result}")  # noqa: T201

    @abstractmethod
    def translate_string(self):
        """Require translate_string to be implemented."""
        raise NotImplementedError

    def __repr__(self):
        """Repr the child classes."""
        return f"{self.__class__.__name__}({self.target_locale.lower()})"
