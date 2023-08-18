# -*- coding: utf-8 -*-
import os
import time
import json
from urllib import request, parse
from .base import BaseTranslator
from settings import DEEPL_API_ENDPOINT


class DeepLTranslator(BaseTranslator):
    """DeepL translator class."""

    def translate_string(self, text: str) -> str:
        """Translate a specifig string.

        Test with curl:
        $ curl https://api-free.deepl.com/v2/translate \
            -d auth_key=YOUR-API-KEY-HERE \
            -d "text=Hello, world!" \
            -d "target_lang=ES"

        :param text: string to translate
        :return: string translation
        """
        if not isinstance(text, str):
            return text

        cached_result = self.cached.get(text)
        if cached_result:
            self.log_translation(
                input_text=text,
                result=f"{cached_result} (cached)",
            )
            return cached_result

        time.sleep(self.sleep)

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

        self.log_translation(
            input_text=text,
            result=response_data["translations"][0]["text"],
            status=self.Status.success,
        )

        dec_text = self.decode_text(
            text=response_data["translations"][0]["text"],
        )

        self.cached[text] = dec_text

        return dec_text
