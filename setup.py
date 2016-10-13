# coding: utf-8

from setuptools import setup, find_packages

import mangasproject

try:
    with open('requirements.txt') as f:
        requirements = [l for l in f.read().splitlines() if l]

    with open('README.md') as readme:
        long_description = readme.read()
except IOError:
    long_description = mangasproject.__description__
    requirements = [
        'requests',
        'tabulate',
    ]

SETUP_ARGS = {
    'name':                 mangasproject.__title__,
    'description':          mangasproject.__description__,
    'long_description':     long_description,
    'version':              mangasproject.__version__,
    'author':               mangasproject.__author__,
    'url':                  mangasproject.__url__,
    'keywords':             'manga, downloader, mangásPROJECT',
    'include_package_data': True,
    'zip_safe':             False,
    'license':              'Apache-2.0',
    'platforms':            'any',
    'install_requires':     requirements,
    'classifiers':          [
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    'entry_points':          {
        'console_scripts': [
            'mangasproject = mangasproject.__main__:main'
        ]
    },
    'packages':              find_packages(),
}

if __name__ == '__main__':
    setup(**SETUP_ARGS)