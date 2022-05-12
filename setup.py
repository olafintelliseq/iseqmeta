from distutils.command.install_lib import install_lib
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='iseqmeta',
    version='0.0.1',
    description='Meta data for intelliseq',
    py_modules=['google_spreadsheet_to_meta_workflows'],
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "gspread"
    ],
    extras_require={
        "dev": [
            "pytest>=3.7"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ]
)