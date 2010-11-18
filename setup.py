#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = 'tstable',
    version = '0.1',
    author = 'James Arthur',
    author_email = 'thruflo@geemail.com',
    url = 'http://github.com/thruflo/tstable',
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Framework :: Paste',
        'Framework :: Zope3',
        'License :: Public Domain'
    ],
    license = 'http://creativecommons.org/publicdomain/zero/1.0/',
    packages = ['tstable'],
    package_dir = {'': 'src'},
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'nose==0.11.2',
        'coverage==3.4',
        'setuptools_git==0.3.4',
        'gunicorn==0.11.2', #'>=0.9.1',
        'PasteScript==1.7.3',
        'zope.interface==3.6.1',
        'zope.component==3.10.0'
    ],
    entry_points = {
        'setuptools.file_finders': [
            "foobar = setuptools_git:gitlsfiles"
        ],
        'paste.app_factory': [
            'main=testable.main:app_factory'
        ]
    }
)
