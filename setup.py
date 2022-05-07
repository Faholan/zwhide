"""Setup options for installing the package."""

import os
import sys
import re

from setuptools import setup


with open("zwhide/__init__.py", encoding="utf-8") as file:
    match = re.search(
        r"^__version__\s*=\s*['\"]([^'\"]*)['\"]",
        file.read(),
        re.MULTILINE,
    )
    version = match.group(1) if match else ""

if not version:
    raise RuntimeError("Version is not set")


with open("README.md", encoding="utf-8") as file:
    readme = file.read()


use_mypyc = os.getenv("USE_MYPYC", None) == "1"

if len(sys.argv) > 1 and sys.argv[1] == "--use-mypyc":
    sys.argv.pop(1)
    use_mypyc = True  # pylint: disable=invalid-name


if use_mypyc:
    from mypyc.build import mypycify  # pylint: disable=no-name-in-module
    ext_modules = mypycify(
        [
            "zwhide/__init__.py",
            "zwhide/hide.py",
            "--disallow-untyped-defs",
            "--disallow-incomplete-defs",
            "--strict-equality",
        ]
    )
else:
    ext_modules = []


setup(
    version=version,
    long_description=readme,
    long_description_content_type="text/markdown",
    ext_modules=ext_modules,
)
