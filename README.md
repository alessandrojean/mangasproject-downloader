# mangásPROJECT Downloader
[![Build Status](https://travis-ci.org/alessandrojean/mangasproject-downloader.svg?branch=master)](https://travis-ci.org/alessandrojean/mangasproject-downloader)

Simple downloader of mangásPROJECT website.

## Instalation
    git clone https://github.com/alessandrojean/mangasproject-downloader
    cd mangasproject
    [sudo] python setup.py install
    
## How to use
Search
    
    mangasproject --search "one piece"
List chapters of a series by id

    mangasproject --id 13 --list-chapters [--page 2]
Download chapters by number

    mangasproject --id 13 --chapters "831,832,833" [--page 2] --download

All examples can be found at [Commands](https://github.com/alessandrojean/mangasproject-downloader/wiki/Commands) page.
## Observations

+ All the chapters will be downloaded in the `/export` folder;
+ The filename of the chapters will be `[<scanlator>] <series_name> <chapter_number>.zip`

## Requirements
+ **[tabulate](https://pypi.python.org/pypi/tabulate)** *v0.7.5+*
+ **[requests](https://pypi.python.org/pypi/requests/)** *v2.9.1+*

## License

    Copyright 2016 Alessandro Jean

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
## Disclaimer

The developer of this library don't have anny filiation with the involved site.