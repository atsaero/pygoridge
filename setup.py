#!/usr/bin/env python3
from setuptools import setup, find_packages


setup(
    name='pygoridge',
    version='1.0.0',
    author='Maksim Ryndin',
    author_email='ryndin@atsaero.ru',
    url='TODO',
    description='Python client for Goridge',

    license='MIT',
    packages=find_packages(exclude=("tests", "examples")),
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
