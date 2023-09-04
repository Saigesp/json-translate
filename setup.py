# -*- coding: utf-8 -*-
import sys
import setuptools
from pathlib import Path

if sys.version_info.major == 2:
    sys.exit("Python 2 is not supported anymore. The last supported version is 3.10.0")

BASE_DIR = Path(__file__).resolve().parent
version = "{{VERSION_PLACEHOLDER}}"

with Path.open(BASE_DIR / "README.md") as fh:
    long_description = fh.read()


def get_reqs(filename):
    """Read file per-line."""
    with Path.open(BASE_DIR / filename) as reqs_file:
        return reqs_file.readlines()


reqs = get_reqs("requirements.txt")

setuptools.setup(
    name="json_translate",
    version=version,
    author="Saigesp",
    author_email="saigesp@gmail.com",
    description="CLI tool to translate json files using different external services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.10",
    install_requires=reqs,
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
    ],
    entry_points={
        "console_scripts": [
            "json_translate=json_translate.commands:main",
        ],
    },
)
