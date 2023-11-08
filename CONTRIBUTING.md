# Welcome to json-translate contributing guide

Thank you for investing your time in contributing to this project!

## How to make changes

### Fork and install

1. Fork the repository and clone it.

2. Create virtual environment and install dev dependencies:
```shell
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

3. Install [pre-commit](https://pre-commit.com/) hooks
```shell
pre-commit install
```

4. Create an `.env` file with:
```
DEEPL_AUTH_KEY=your-key-here
```

5. Create a working branch and start with your changes!

### Tests your changes

The tests will run automatically when you commit your changes. However, you can run them before with the command:

```shell
python -m unittest discover -b tests/
```

### Commit your update

Commit the changes once you are happy with them.

### Pull Request

When you're finished with the changes, create a pull request to the main repo.

### Your PR is merged!

Congratulations :tada::tada: And thanks for contributing!
