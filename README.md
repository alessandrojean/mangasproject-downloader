# mangásPROJECT Downloader
[![Build Status](https://travis-ci.org/alessandrojean/mangasproject-downloader.svg?branch=master)](https://travis-ci.org/alessandrojean/mangasproject-downloader)
Simple downloader of mangásPROJECT website.

## Instalation
    git clone https://github.com/alessandrojean/mangasproject-downloader
    cd mangasproject
    [sudo] python setup.py install
    
## How to use
Search
    
    mangasproject --search="one piece"
List chapters of a series by id

    mangasproject --id=13 --chapters [--page=2]
Download chapters by id

    mangasproject --ids=12345,67890 --download

## Observations

+ All the chapters will be downloaded in the */export* folder.
+ Unfortunately, the mangásPROJECT API doesn't provide an search by id, so now the downloaded chapters file name is *&lt;release_id&gt;.zip*

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

The developer of this library don't have anny filiation with the involved sites.