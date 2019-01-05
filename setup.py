#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import io
import re

from setuptools import setup

RE_BADGE = re.compile(r'^\[\!\[(?P<text>.*?)\]\((?P<badge>.*?)\)\]\((?P<target>.*?)\)$', re.M)

BADGES_TO_KEEP = []


def md(filename):
    '''Load .md (markdown) file and sanitize it for PyPI.'''
    content = io.open(filename).read()

    for match in RE_BADGE.finditer(content):
        if match.group('badge') not in BADGES_TO_KEEP:
            content = content.replace(match.group(0), '')

    return content


def pip(filename):
    '''Parse pip reqs file and transform it to setuptools requirements.'''
    return open(os.path.join('requirements', filename)).readlines()


long_description = '\n'.join((
    md('README.md'),
    md('CHANGELOG.md'),
    ''
))

install_requires = pip('install.pip')
tests_require = pip('develop.pip')


setup(
    name='tox-asdf',
    version=__import__('tox_asdf').__version__,
    description=__import__('tox_asdf').__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/apihackers/tox-asdf',
    author='API Hackers',
    author_email='pypi+tox-asdf@apihackers.com',
    packages=['tox_asdf'],
    # python_requires='==2.7.*',
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
    },
    entry_points={
        'tox': ['asdf = tox_asdf.plugin'],
    },
    license='MIT',
    zip_safe=False,
    keywords='tox asdf',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development',
    ],
)
