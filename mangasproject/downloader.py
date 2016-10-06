# coding: utf-8
import os
import zipfile
from urlparse import urlparse
import requests

from mangasproject.utils import Singleton
from mangasproject.logger import logger
from mangasproject.api import request, list_pages


class Downloader(Singleton):
    def __init__(self, timeout=30):
        self.timeout = timeout

    def _download(self, url, folder='', filename='', retried=False):
        logger.info("Start downloading: {0} ...".format(url))
        filename = filename if filename else os.path.basename(urlparse(url).path)
        base_filename, extension = os.path.splitext(filename)
        try:
            with open(os.path.join(folder, base_filename.zfill(3)+extension), "wb") as f:
                response = request("get", url, stream=True, timeout=self.timeout)
                length = response.headers.get("content-length")
                if length is None:
                    f.write(response.content)
                else:
                    for chunk in response.iter_content(2048):
                        f.write(chunk)
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

    def _zipdir(self, id_release):
        logger.info("Creating {0}.zip".format(id_release))
        zipf = zipfile.ZipFile("export/{0}.zip".format(id_release), "w", zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk("export/{0}/".format(id_release)):
            for file in files:
                zipf.write(os.path.join(root, file))
                os.remove(os.path.join(root, file))
        logger.info("Deleting folder \'{0}\'".format(id_release))
        os.rmdir("export/{0}".format(id_release))
        zipf.close()

    def download(self, chapter):
        list_pages(chapter)

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

        for url in chapter.pages:
            self._download(url, folder=folder)

        self._zipdir(chapter.id_release)
