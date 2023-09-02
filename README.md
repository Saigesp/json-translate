# json-deepl-translate

CLI tool to translate json files automatically using Deepl API

<a href="https://github.com/Saigesp/json-deepl-translate/issues">
  <img src="https://img.shields.io/github/issues-raw/Saigesp/json-deepl-translate" alt="Open issues">
</a>
<a href="https://github.com/Saigesp/json-deepl-translate/pulls">
  <img src="https://img.shields.io/github/issues-pr-raw/Saigesp/json-deepl-translate" alt="Open PRs">
</a>
<a href="https://github.com/Saigesp/json-deepl-translate/blob/master/LICENSE.md">
  <img src="https://img.shields.io/github/license/Saigesp/json-deepl-translate" alt="License">
</a>
<a href="https://github.com/Saigesp/json-deepl-translate/releases">
  <img src="https://img.shields.io/github/v/release/Saigesp/json-deepl-translate" alt="Release">
</a>
<a href="https://github.com/Saigesp/json-deepl-translate/graphs/contributors">
  <img src="https://img.shields.io/github/contributors/Saigesp/json-deepl-translate" alt="Contributors">
</a>
<a href="https://github.com/Saigesp/json-deepl-translate/commits/master">
  <img src="https://img.shields.io/github/last-commit/Saigesp/json-deepl-translate/master" alt="Commits">
</a>

Usually multi-language projects developed with a javascript framework (Angular, Vue...) base their translations on json files with different nesting levels. This small project allows you to generate new files for other languages while keeping the same structure.

The supported languages are [the same as DeepL](https://www.deepl.com/docs-api/translate-text).

Requires **Python version >= 3.10**

```shell
python json_translate /path/to/file/en_US.json --locale FR
```

## Install
1. Clone this repository.
2. Create a virtual environment.
3. Install dependencies:
```shell
pip install -r requirements.txt
```
4. Create an `.env` file with:
```
DEEPL_AUTH_KEY=your-key-here
```
> You can get a free deepl developer account in https://www.deepl.com/pro-checkout/account (Credit card needed)

If you wish to upgrade to a paid account, you will need to add the paid api endpoint in the `.env` file:
```
DEEPL_API_ENDPOINT=https://api.deepl.com/v2/translate
```

Other parameters can also be overwritten:
```
SLEEP_BETWEEN_API_CALLS=0.01
INDENTATION_DEFAULT=2
ENCODING=utf-8
```

## Usage
1. Execute the command with the file path and the language you want to generate

```shell
python json_translate /home/user/project/locales/en_US.json --locale ES --output es_ES.json
```
> The script will create an `es_ES.json` file in the same folder as the source file.

### Optional parameters

```
-l, --locale          Target language to translate the file. Defaults to "en" (English)
-sl, --source-locale  Source language translating from (Optional, required for glossaries)
-g, --glossary        Glossary ID to use when translating (Optional)
-o, --output          Output file name. Defaults to "<target locale>.json" (ex: en.json)
-e, --extend          Extend an existing translation file (defined by output file name)
-s, --sleep           Sleep time between API calls. Defaults to 0.01 (seconds)
-i, --indent          Output file indentation spaces. Defaults to 2
--encoding            Input & output file encoding. Defaults to UTF-8
--skip                Keys to skip in the json file (they won't be translated)
--log                 Display translations as they are being translated
```
> Note that **sleep**, **indentation** and **encoding** can also be defined with variables in the `.env` file but they are overwritten with the values of the command.

### Example file
Translate the example file `/tests/data/en_US.json` to spanish:
```shell
python json_translate tests/data/en_US.json --locale ES --skip lorem ipsum --log
```

## API usage
You can check your API usage with
```shell
curl -H "Authorization: DeepL-Auth-Key YOUR-API-KEY-HERE" https://api-free.deepl.com/v2/usage
```

## Contributing
See the [contributing guide](CONTRIBUTING.md) for detailed instructions on how to get started.

## License
This repository is available under [**GNU LESSER GENERAL PUBLIC LICENSE v2.1** (LGPL)](LICENSE.md).
