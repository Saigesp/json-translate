# -*- coding: utf-8 -*-
import os

# DeppL API endpoint
DEEPL_API_ENDPOINT = os.environ.get(
    "DEEPL_API_ENDPOINT",
    "https://api-free.deepl.com/v2/translate",
)

# Seconds to sleep between API calls
SLEEP_BETWEEN_API_CALLS = float(os.environ.get("SLEEP_BETWEEN_API_CALLS", 0.01))

# Default indentation to output the json file
INDENTATION_DEFAULT = int(os.environ.get("INDENTATION_DEFAULT", 2))

# Default input file encoding
ENCODING = os.environ.get("ENCODING", "utf-8")

# Global cache
GLOBAL_CACHE = dict()

# Supported language codes
# https://www.deepl.com/docs-api/translate-text
# fmt: off
SUPPORTED_LANG_CODES = (
    'BG', 'CS', 'DA', 'DE', 'EL', 'EN', 'EN-GB', 'EN-US', 'ES', 'ET', 'FI', 'FR', 'HU', 'ID',
    'IT', 'JA', 'LT', 'LV', 'NL', 'PL', 'PT-PT', 'PT-BR', 'RO', 'RU', 'SK', 'SL', 'SV',
    'TR', 'UK', 'ZH',
)
# fmt: on
