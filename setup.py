#!/usr/bin/env python
import sys
from subprocess import check_call

from setuptools import setup, find_packages
from setuptools.command.install import install
# from Cython.Build import cythonize


# class PostInstallCommand(install):
#     """Post-installation for installation mode."""
#     def run(self):
#         check_call("python setup.py build_ext --inplace".split())
#         install.run(self)


setup(
    name='pygoridge',
    version='0.1.0',
    author='Maksim Ryndin',
    author_email='ryndin@atsaero.ru',
    url='TODO',
    description='Python client for Goridge',

    license='MIT',
    packages=find_packages(exclude=("tests", "scripts")),
    # ext_modules=cythonize([
    #     "src/*.py"
    #     ]),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: Russian',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ]
)
