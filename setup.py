#!/usr/bin/env python
from distutils.core import setup
from os import path

setup(
    name = 'bambu-comments',
    version = '2.0',
    description = 'Generic model commenting',
    author = 'Steadman',
    author_email = 'mark@steadman.io',
    url = 'https://github.com/iamsteadman/bambu-comments',
    long_description = open(path.join(path.dirname(__file__), 'README')).read(),
    install_requires = [
        'Django>=1.4',
        'pyquery',
        'html2text',
        'markdown',
        'bambu-mail>=2.0',
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
            'templates/search/indexes/comments/*.txt'
        ]
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django'
    ]
)