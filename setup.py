#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs

from setuptools import setup, find_packages


def rst(filename):
    return codecs.open(filename, encoding='utf-8').read()


long_description = '\n'.join((
    rst('README.rst'),
    rst('CHANGELOG.rst'),
    ''
))

setup(
    name='django.js',
    version=__import__('djangojs').__version__,
    description=__import__('djangojs').__description__,
    long_description=long_description,
    url='https://github.com/noirbizarre/django.js',
    download_url='http://pypi.python.org/pypi/django.js',
    author='Axel Haustant',
    author_email='noirbizarre+django@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    license='LGPL',
    # use_2to3=True,
    keywords='django javascript test url reverse helpers',
    classifiers=[
        "Framework :: Django",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: System :: Software Distribution",
        "Programming Language :: Python",
        'Programming Language :: Python :: 3',
        "Topic :: Software Development :: Libraries :: Python Modules",
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    ],
)
