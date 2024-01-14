# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

load_dotenv()

DEEPL_API_ENDPOINT = os.getenv(
    "DEEPL_API_ENDPOINT",
    "https://api-free.deepl.com/v2/translate",
)
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Seconds to sleep between API calls
SLEEP_BETWEEN_API_CALLS = float(os.getenv("SLEEP_BETWEEN_API_CALLS", 0.01))

# Default indentation to output the json file
INDENTATION_DEFAULT = int(os.getenv("INDENTATION_DEFAULT", 2))

# Default input file encoding
ENCODING = os.getenv("ENCODING", "utf-8")

# Supported language codes
# fmt: off
DEELP_SUPPORTED_LANGS = ( # https://www.deepl.com/docs-api/translate-text
    "BG", "CS", "DA", "DE", "EL", "EN", "EN-GB", "EN-US", "ES", "ET", "FI", "FR", "HU", "ID",
    "IT", "JA", "KO", "LT", "LV", "NB", "NL", "PL", "PT-BR", "PT-PT", "RO", "RU", "SK",
    "SL", "SV", "TR", "UK", "ZH",
)

AWS_SUPPORTED_LANGS = ( # https://docs.aws.amazon.com/translate/latest/dg/what-is-languages.html
    "af", "sq", "am", "ar", "hy", "az", "bn", "bs", "bg", "ca", "zh", "zh-TW", "hr", "cs",
    "da", "fa-AF", "nl", "en", "et", "fa", "tl", "fi", "fr", "fr-CA", "ka", "de", "el",
    "gu", "ht", "ha", "he", "hi", "hu", "is", "id", "ga", "it", "ja", "kn", "kk", "ko",
    "lv", "lt", "mk", "ms", "ml", "mt", "mr", "mn", "no", "ps", "pl", "pt", "pt-PT", "pa",
    "ro", "ru", "sr", "si", "sk", "sl", "so", "es", "es-MX", "sw", "sv", "ta", "te", "th",
    "tr", "uk", "ur", "uz", "vi", "cy",
)
# fmt: on
