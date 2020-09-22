#!/usr/bin/env python

from setuptools import setup, find_packages
from one.__init__ import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    'altgraph==0.17',
    'certifi==2020.4.5.1',
    'chardet==3.0.4',
    'click==7.1.2',
    'docker-py==1.10.6',
    'docker-pycreds==0.4.0',
    'dockerpty==0.4.1',
    'idna==2.9',
    'prompt-toolkit==1.0.14',
    'Pygments==2.6.1',
    'PyInquirer==1.0.3',
    'PyInstaller==3.6',
    'python-dotenv==0.13.0',
    'PyYAML==5.3.1',
    'regex==2020.5.7',
    'requests==2.23.0',
    'six==1.14.0',
    'urllib3==1.25.9',
    'wcwidth==0.1.9',
    'websocket-client==0.57.0',
    'packaging==20.4'
]

setup(
    name='one-cli',
    version=__version__,
    py_modules=['one'],
    include_package_data=True,
    description='Python CLI to manage stacks from DNX.',
    license="Apache License 2.0",
    url='https://github.com/DNXLabs/one-cli',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='DNX Solutions',
    author_email='contact@dnx.solutions',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    packages=find_packages(),
    install_requires=install_requires,
    python_requires='>=3.6',
    entry_points='''
        [console_scripts]
        one=one.__main__:main
    ''',
)
