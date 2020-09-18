#!/usr/bin/env python3
from setuptools import setup, find_packages


setup(
    name='pygoridge',
    version='0.1.0',
    author='Maksim Ryndin',
    author_email='ryndin@atsaero.ru',
    url='https://github.com/atsaero/pygoridge',
    description='Python client for Goridge',

    license='MIT',
    packages=find_packages(exclude=("tests", "examples", "goridge")),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Natural Language :: Russian',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
