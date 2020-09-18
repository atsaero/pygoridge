#!/usr/bin/env python3
import os.path
from setuptools import setup, find_packages


def get_description():
    README = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')
    with open(README, 'r') as f:
        return f.read()


setup(
    name='pygoridge',
    version='0.1.0',
    author='Maksim Ryndin',
    author_email='ryndin@atsaero.ru',
    url='https://github.com/atsaero/pygoridge',
    description='Python-Golang IPC bridge, python client for Goridge',
    long_description=get_description(),
    license='MIT',
    packages=find_packages(exclude=("tests", "examples", "goridge")),
    python_requires='>=3.6',
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
