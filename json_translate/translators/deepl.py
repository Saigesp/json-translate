# -*- coding: utf-8 -*-
import os
import json
from urllib import request, parse
from .base import BaseTranslator
from settings import DEEPL_API_ENDPOINT


class DeepLTranslator(BaseTranslator):
    """DeepL translator class."""

    def __init__(self, *args, **kwargs):
        """Initialize DeepL translator instance.

        :param **kwargs:
            glossary: Glossary ID to use when translating
        """
        self.glossary = kwargs.get("glossary")
        super().__init__(*args, **kwargs)

    def translate_string(self, text: str) -> str:
        """Translate a specifig string.

        :param text: string to translate
        :return: string translation
        """
        data = {
            "target_lang": self.target_locale,
            "auth_key": os.environ.get("DEEPL_AUTH_KEY"),
            "text": text,
            "preserve_formatting": "1",
        }

        if self.source_locale is not None:
            data["source_lang"] = self.source_locale

        if self.glossary is not None:
            data["glossary_id"] = self.glossary

        data = parse.urlencode(data).encode()

        req = request.Request(DEEPL_API_ENDPOINT, data=data)
        response = request.urlopen(req)  # nosec

        if response.status != 200:
            self.log_translation(
                input_text=text,
                result=f"response status: {response.status}",
                status=self.Status.error,
            )
            return text

        response_data = json.loads(response.read())

        if "translations" not in response_data:
            self.log_translation(
                input_text=text,
                result=f"response empty: {response_data}",
                status=self.Status.error,
            )
            return text

        if len(response_data["translations"]) > 1:
            self.log_translation(
                input_text=text,
                result=f"more than 1 translation: {response_data['translations']})",
                status=self.Status.warning,
            )

        return response_data["translations"][0]["text"]
