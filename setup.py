#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from setuptools import Command, setup
from setuptools.command.test import test as TestCommand

with open('README.rst') as readme_file:
    readme = readme_file.read()


requirements = [
]

test_requirements = [
    'pytest'
]


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='python-logging-json-formatter',
    version='0.1.0',
    description="A logging formatter that appends extra data as JSON, e.g. for loggly",
    long_description=readme,
    author='Opbeat, Inc',
    author_email='support@opbeat.com',
    url='https://github.com/opbeat/python-logging-json-formatter',
    packages=[
        'logging_json_formatter',
    ],
    package_dir={'logging_json_formatter':
                 'logging_json_formatter'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='logging, json, loggly',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    cmdclass={'test': PyTest},
)
