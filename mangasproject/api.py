import requests
import re

from mangasproject.logger import logger
from mangasproject.constants import SEARCH_URL, CHAPTERS_LIST_URL, PAGES_LIST_URL, USER_AGENT
from mangasproject.series import Series, Category, Chapter


def request(method, url, **kwargs):
    if not hasattr(requests, method):
        raise AttributeError('\'requests\' object has no attribute \'{0}\''.format(method))

    headers = {"X-Requested-With": "XMLHttpRequest", "User-Agent": USER_AGENT}
    return requests.__dict__[method](url, headers=headers, **kwargs)


def search(query):
    results = []

    logger.info(u"Searching for {0}".format(query))

    data = {"search": query}
    try:
        resp = request('post', SEARCH_URL, json=data).json()
    except Exception as e:
        logger.critical(str(e))
        exit(1)

    for serie in resp["series"]:
        s = Series(serie["id_serie"])
        s.name = serie["name"]
        s.label = serie["label"]
        s.score = serie["score"]
        s.value = serie["value"]
        s.artist = serie["artist"]
        s.author = serie["author"]
        s.cover = serie["cover"]
        s.is_complete = serie["is_complete"]
        s.link = serie["link"]

        for category in serie["categories"]:
            c = Category(category["id_category"])
            c.id_sub_domain = category["id_sub_domain"]
            c.domain = category["domain"]
            c.name = category["name"]

            s.categories.append(c)

        results.append(s)

    return results


def list_chapters(series, page=1):
    logger.info(u"Fetching chapters of {0}".format(series.id))

    data = {"id_serie": series.id}
    url = "{0}{1}".format(CHAPTERS_LIST_URL, page)
    try:
        resp = request('post', url, json=data).json()
    except Exception as e:
        logger.critical(str(e))
        exit(1)

    for chapter in resp["chapters"]:
        c = Chapter(chapter["id_chapter"])
        c.id_series = chapter["id_serie"]
        c.series_name = chapter["name"]
        c.name = chapter["chapter_name"]
        c.number = chapter["number"]
        c.date = chapter["date"]
        c.scanlator = chapter["scanlator"]
        c.partner_scans = chapter["partner_scans"]
        c.view_count = chapter["view_count"]
        c.link = chapter["link"]

        m = re.search("([0-9]+)-(.*)$", c.link)
        c.id_release = m.group(1)

        series.chapters.append(c)


def list_pages(chapter):
    logger.info(u"Fetching pages of {0}".format(chapter.id_release))

    data = {"id_release": chapter.id_release}
    try:
        resp = request('post', PAGES_LIST_URL, json=data).json()
    except Exception as e:
        logger.critical(str(e))
        exit(1)

    chapter.pages = resp["images"]


if __name__ == "__main__":
    gantz = search("Gantz")[0]
    gantz.show()
    list_chapters(gantz)
    gantz.chapters[0].show()