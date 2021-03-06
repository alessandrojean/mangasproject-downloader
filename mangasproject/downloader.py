# coding: utf-8
import os
import zipfile
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import requests

from mangasproject.utils import Singleton
from mangasproject.logger import logger
from mangasproject.api import request, list_pages
from mangasproject.cmdline import print_progress
from mangasproject.constants import URL


class Downloader(Singleton):
    def __init__(self, timeout=30, webp=True):
        self.timeout = timeout
        self.webp = webp

    def _download(self, url, folder='', filename='', retried=False, iteration=0, total=0):
        url = URL + url if url.startswith('/') else url
        filename = filename if filename else os.path.basename(urlparse(url).path)
        base_filename, extension = os.path.splitext(filename)
        try:
            with open(os.path.join(folder, base_filename.zfill(3)+extension), "wb") as f:
                response = request("get", url, stream=True, timeout=self.timeout)
                length = response.headers.get("content-length")
                if length is None:
                    f.write(response.content)
                else:
                    dl = 0
                    for chunk in response.iter_content(2048):
                        dl += len(chunk)
                        f.write(chunk)
                        print_progress(iteration, total, file_iteration=dl, file_total=int(length), prefix='[PROGRESS]', suffix='Complete', bar_length=50)
        except requests.HTTPError as e:
            if not retried:
                logger.error("Error: {0}, retrying".format(str(e)))
                return self._download(url=url, folder=folder, filename=filename, retried=True)
            else:
                return None
        except Exception as e:
            if not retried:
                logger.error("Error: {0}, retrying".format(str(e)))
                return self._download(url=url, folder=folder, filename=filename, retried=True)
            else:
                return None
        return url

    def _rem_ilegal_characters(self, text):
        return "".join(x for x in text if (x.isalnum() or x in "._- "))

    def _zipdir(self, chapter):
        chapter.scanlator = self._rem_ilegal_characters(chapter.scanlator)
        chapter.series.name = self._rem_ilegal_characters(chapter.series.name)

        filename = "[{0}] {1} {2}.zip".format(
            chapter.scanlator, chapter.series.name, chapter.number
        )
        logger.info("Creating \'{}\'".format(filename))
        zipf = zipfile.ZipFile("export/{}".format(filename), "w", zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk("export/{}/".format(chapter.id_release)):
            for file in files:
                zipf.write(os.path.join(root, file))
                os.remove(os.path.join(root, file))
        logger.info("Deleting folder \'{0}\'".format(chapter.id_release))
        os.rmdir("export/{0}".format(chapter.id_release))
        zipf.close()

    def download(self, chapter):
        list_pages(chapter, webp=self.webp)

        folder = 'export/{0}'.format(str(chapter.id_release))

        if not os.path.exists(folder):
            logger.warn("Path \'{0}\' not exist.".format(folder))
            try:
                os.makedirs(folder)
            except EnvironmentError as e:
                logger.critical('Error: {0}'.format(str(e)))
                exit(1)
        else:
            logger.warn("Path \'{0}\' already exist.".format(folder))

        i = 0
        t = len(chapter.pages)
        print_progress(i, t, prefix='[PROGRESS]', suffix='Complete', bar_length=50)
        for url in chapter.pages:
            self._download(url, folder=folder, iteration=i, total=t)
            i += 1
            print_progress(i, t, prefix='[PROGRESS]', suffix='Complete', bar_length=50)

        self._zipdir(chapter)
