# -*- coding: utf-8 -*-
import boto3
from .base import BaseTranslator
from settings import (
    AWS_REGION_NAME,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
)


class AWSTranslator(BaseTranslator):
    """AWS translator class."""

    def __init__(self, *args, **kwargs):
        """Initialize AWS translator instance.

        :param **kwargs:
            formality: level of formality for translations
            profanity: mask profane words and phrases
        """
        self.client = boto3.client(
            "translate",
            region_name=AWS_REGION_NAME,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        self.formality = kwargs.get("formality")
        self.profanity = kwargs.get("profanity")

        if kwargs.get("source_locale") is None:
            raise Exception("Param 'source_locale' is required in AWSTranslator")

        super().__init__(*args, **kwargs)

    def translate_string(self, text: str) -> str:
        """Translate a specifig string.

        :param text: string to translate
        :return: string translation
        """
        settings = {}

        if self.formality is not None:
            settings["Formality"] = self.formality.upper()

        if self.profanity is not None:
            settings["Profanity"] = self.profanity.upper()

        response = self.client.translate_text(
            Text=text,
            SourceLanguageCode=self.source_locale,
            TargetLanguageCode=self.target_locale,
            Settings=settings,
        )

        meta = response.get("ResponseMetadata")

        if meta.get("HTTPStatusCode") != 200:
            self.log_translation(
                input_text=text,
                result=f"response status: {meta.get('HTTPStatusCode')}",
                status=self.Status.error,
            )
            return text

        if not response.get("TranslatedText"):
            self.log_translation(
                input_text=text,
                result=f"response empty: {response}",
                status=self.Status.error,
            )
            return text

        return response.get("TranslatedText")
