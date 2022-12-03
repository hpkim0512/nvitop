#!/usr/bin/env python3

# To install `nvitop` with specific version of `nvidia-ml-py`, use:
#
#   pip install nvidia-ml-py==xx.yyy.zz nvitop
#
# or
#
#   pip install 'nvitop[pynvml-xx.yyy.zz]'
#

# pylint: disable=missing-module-docstring

import pathlib
import re
import sys

from setuptools import setup


HERE = pathlib.Path(__file__).absolute().parent
VERSION_FILE = HERE / 'nvitop' / 'version.py'

sys.path.insert(0, str(VERSION_FILE.parent))
# pylint: disable-next=import-error,wrong-import-position
import version  # noqa


VERSION_CONTENT = None

try:
    if not version.__release__:
        try:
            VERSION_CONTENT = VERSION_FILE.read_text(encoding='UTF-8')
            VERSION_FILE.write_text(
                data=re.sub(
                    r"""__version__\s*=\s*('[^']+'|"[^"]+")""",
                    r"__version__ = '{}'".format(version.__version__),
                    string=VERSION_CONTENT,
                ),
                encoding='UTF-8',
            )
        except OSError:
            VERSION_CONTENT = None

    setup(
        name='nvitop',
        version=version.__version__,
        extras_require={
            'lint': [
                'black >= 22.6.0',
                'isort',
                'pylint[spelling] >= 2.15.0, != 2.16, != 2.17',
                'pre-commit',
            ],
            'cuda10': ['nvidia-ml-py == 11.450.51'],
            **{
                # The identifier could not start with numbers, add a prefix `pynvml-`
                'pynvml-{}'.format(pynvml): ['nvidia-ml-py == {}'.format(pynvml)]
                for pynvml in version.PYNVML_VERSION_CANDIDATES
            },
        },
    )
finally:
    if VERSION_CONTENT is not None:
        VERSION_FILE.write_text(data=VERSION_CONTENT, encoding='UTF-8')
