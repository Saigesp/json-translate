# -*- coding: utf-8 -*-
from .deepl import DeepLTranslator
from .aws import AWSTranslator


def get_translator(service: str):
    """Get translator service class."""
    if service == "aws":
        return AWSTranslator

    return DeepLTranslator
