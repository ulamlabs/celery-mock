#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

import celery_mock

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'celery',
    'mock',
]

test_requirements = [
]

setup(
    name='celery-mock',
    version=celery_mock.__version__,
    description=(
        "celery-mock allows you to mock celery task "
        "and then run them when you want"
    ),
    long_description=readme + '\n\n',
    author="Konrad Rotkiewicz",
    author_email='konrad@ulam.io',
    url='https://github.com/ulamlabs/celery-mock',
    packages=[
        'celery_mock',
    ],
    package_dir={'celery_mock':
                 'celery_mock'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='celery_mock',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
