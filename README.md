# json-translate

CLI tool to translate json files automatically using external translation services like **DeepL** or **AWS Translate**

<a href="https://github.com/Saigesp/json-translate">
  <img alt="" src="https://img.shields.io/badge/python-3.10-blue.svg">
</a>
<a href="https://github.com/Saigesp/json-translate/issues">
  <img src="https://img.shields.io/github/issues-raw/Saigesp/json-translate" alt="Open issues">
</a>
<a href="https://github.com/Saigesp/json-translate/pulls">
  <img src="https://img.shields.io/github/issues-pr-raw/Saigesp/json-translate" alt="Open PRs">
</a>
<a href="https://github.com/Saigesp/json-translate/blob/master/LICENSE.md">
  <img src="https://img.shields.io/github/license/Saigesp/json-translate" alt="License">
</a>
<a href="https://github.com/Saigesp/json-translate/releases">
  <img src="https://img.shields.io/github/v/release/Saigesp/json-translate" alt="Release">
</a>
<a href="https://github.com/Saigesp/json-translate/graphs/contributors">
  <img src="https://img.shields.io/github/contributors/Saigesp/json-translate" alt="Contributors">
</a>
<a href="https://github.com/Saigesp/json-translate/commits/master">
  <img src="https://img.shields.io/github/last-commit/Saigesp/json-translate/master" alt="Commits">
</a>

Usually multi-language projects developed with a javascript framework (Angular, Vue...) base their translations on json files with different nesting levels. This small project allows you to generate new files for other languages while keeping the same structure.

> [!WARNING]
> Requires **Python version >= 3.10**

```shell
json_translate deepl /path/to/file.json FR
```

The supported languages depends on the service used:
- [DeepL supported languages](https://www.deepl.com/docs-api/translate-text).
- [AWS supported languages](https://docs.aws.amazon.com/translate/latest/dg/what-is-languages.html).


## Install
1. Clone this repository.

1. Create a virtual environment.

1. Install dependencies:
    ```shell
    pip install -r requirements.txt
    ```
1. To define the environmental variables, create an `.env` file in the root directory with the required variables, which will vary depending on the external service you will use:
    ```
    EXAMPLE_VARIABLE_NAME=example_variable_value
    ```
    > You can also define them directly in your environment without having to create the `.env` file, it's up to you.

### Use with DeepL

You can use DeepL with a free account or with a paid account.

- **Free account**: You can get a free deepl developer account in https://www.deepl.com/pro-checkout/account (Credit card needed). Once you have registered, you must include your auth key in the `.env` file:
    ```
    DEEPL_AUTH_KEY=your-key-here
    ```

- **Paid account**: If you have a paid account, in addition to including your auth key, you must include the API endpoint in the file.
    ```
    DEEPL_AUTH_KEY=your-key-here
    DEEPL_API_ENDPOINT=https://api.deepl.com/v2/translate
    ```

### Use with AWS Translate

Login on your AWS account and obtain your credentials, the place them in the `.env` file:
```
AWS_REGION_NAME=your-aws-region
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
```

## How to use

Execute the command with the service, the file path and the language you want to generate:

```sh
json_translate <service> <source> <locale>
# Example: json_translate aws locales/en.json ES
```

The script will create an `es.json` file in the same folder as the source file.

### Required parameters
```
service               Translation service to use. Can be "deepl" or "aws"
source                Path to source file (must be a json file)
target_locale         Translation target language code
```

### Optional parameters

```
-sl, --source-locale  Source language translating from (Required for AWS).
-o, --output          Output file name. Defaults to "<target_locale>.json" (ex: en.json)
-e, --extend          Extend the existing translation file (defined by <output>)
-s, --sleep           Sleep time between API calls. Defaults to 0.01 (seconds)
-i, --indent          Output file indentation spaces. Defaults to 2
--encoding            Input & output file encoding. Defaults to UTF-8
--skip                Keys to skip in the json file (they won't be translated)
--log                 Display translations as they are being translated
--override            Force override on output file
```

#### DeepL options
```
-g, --glossary        Glossary ID to use when translating (Optional)
```

#### AWS Translate options
```
--formality           Level of formality for translations
--profanity           Mask profane words and phrases
```

Note that **sleep**, **indentation** and **encoding** can also be defined with variables in the `.env` file but they are overwritten with the values of the command:

```
SLEEP_BETWEEN_API_CALLS=0.01
INDENTATION_DEFAULT=2
ENCODING=utf-8
```


### Example file
Translate the example file `/tests/data/en_US.json` to spanish:
```shell
json_translate deepl tests/data/en_US.json ES --skip lorem ipsum --log
```

## DeepL API usage
You can check your API usage with
```shell
curl -H "Authorization: DeepL-Auth-Key YOUR-API-KEY-HERE" https://api-free.deepl.com/v2/usage
```

## Contributing
See the [contributing guide](CONTRIBUTING.md) for detailed instructions on how to get started.

## License
This repository is available under [**GNU LESSER GENERAL PUBLIC LICENSE v2.1** (LGPL)](LICENSE.md).
