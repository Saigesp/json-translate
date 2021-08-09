# json-deepl-translate

Translate json files with deepl API

- Python 3 required

Exmples:
```
python main.py /path/to/locales
python main.py /path/to/file/en.json -l es
python main.py /path/to/file/en_US.json --locale es --output es_ES.json --indent 2
```
> See more options with `python main.py --help`

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
> You can get a free deepl developer account in https://www.deepl.com/pro-checkout/account
