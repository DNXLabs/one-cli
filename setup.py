#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name                          = 'one',
    version                       = '0.0.1',
    py_modules                    = ['one'],
    include_package_data          = True,
    description                   = 'Python CLI to manage stacks from DNX.',
    license                       = 'Apache 2.0',
    url                           = 'https://github.com/DNXLabs/one',
    long_description              = long_description,
    long_description_content_type = "text/markdown",
    author                        = 'DNX Solutions',
    author_email                  = 'contact@dnx.solutions',
    classifiers                   = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"
    ],
    packages                      = ["one"],
    python_requires               = '>=3.6',
    entry_points='''
        [console_scripts]
        one=one.__main__:main
    ''',
)