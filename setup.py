#!/usr/bin/env python
from setuptools import setup
from os import path

setup(
    name = 'bambu-comments',
    version = '3.2',
    description = 'Generic model commenting',
    author = 'Steadman',
    author_email = 'mark@steadman.io',
    url = 'https://github.com/iamsteadman/bambu-comments',
    long_description = open(path.join(path.dirname(__file__), 'README')).read(),
    install_requires = [
        'Django>=1.8',
        'pyquery',
        'html2text',
        'markdown',
        'bambu-mail>=3.0',
        'requests>=2.2.1'
    ],
    packages = [
        'bambu_comments',
        'bambu_comments.templatetags',
        'bambu_comments.migrations'
    ],
    package_data = {
        'bambu_comments': [
            'templates/comments/*.html',
            'templates/comments/*.txt',
            'templates/search/indexes/bambu_comments/*.txt'
        ]
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django'
    ]
)
