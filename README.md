# json-deepl-translate

Translate json files with deepl API

Usually multi-language projects developed with a javascript framework (Angular, Vue...) base their translations on json files with different nesting levels. This small project allows you to generate new files for other languages while keeping the same structure.

- Works with Python3

```shell
python main.py /path/to/file/en_US.json --locale es --output es_ES.json --indent 4 --sleep 0.5
```
> See more options with `python main.py --help`

## Supported languages

You can check the supported languages at this link: [DeepL Translate Text Request Parameters](https://www.deepl.com/docs-api/translate-text) (parameters `source_lang` and `target_lang`)

## Install
1. Create virtual environment

2. Install dependencies:
```shell
pip install -r requirements.txt
```

3. Create an `.env` file with:
```
DEEPL_AUTH_KEY=your-key-here
```
> You can get a free deepl developer account in https://www.deepl.com/pro-checkout/account (Credit card needed)

## Usage
1. Execute the command with the file path and the language you want to generate
```shell
python main.py /home/user/my_project/locales/en_US.json --locale ES --output es_ES.json
```
> The script will create an `es_ES.json` file in the same folder as the source file.

### Optional parameters

```
-l, --locale    Language target to translate. Defaults to "en"
-o, --output    Output file name. Defaults to "en.json
-s, --sleep     Sleep time between API calls. Defaults to 0.01s
-i, --indent    Output file indentation spaces. Defaults to 2
--skip          Keys to skip (they won't be translated)
```

### Example file
Translate the example file `/tests/data/en_US.json` to spanish:
```shell
python main.py tests/data/en_US.json --locale ES --output es_ES.json --skip lorem ipsum
```

## API usage
You can check your API usage with
```shell
curl -H "Authorization: DeepL-Auth-Key YOUR-API-KEY-HERE" https://api-free.deepl.com/v2/usage
```

## Tests
Run tests with:
```shell
python -m unittest discover
```

## License
This repository is available under **GNU LESSER GENERAL PUBLIC LICENSE v2.1** (LGPL). See [details](LICENSE.md).
