# coding: utf-8

from setuptools import setup, find_packages
from mangasproject import __author__, __version__

with open('requirements.txt') as f:
    requirements = [l for l in f.read().splitlines() if l]

setup(
    name='mangasproject-downloader',
    version=__version__,
    packages=find_packages(),
    url='https://alessandrojean.github.io/mangasproject-downloader/',
    license='Apache License',
    author=__author__,
    author_email='',
    description='Simple downloader of mangásPROJECT website.',
    keywords='manga, downloader, mangásPROJECT',
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'mangasproject = mangasproject.__main__:main',
        ]
    },
)
