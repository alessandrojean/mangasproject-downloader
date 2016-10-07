# coding: utf-8
import requests
import re

from mangasproject.logger import logger
from mangasproject.constants import SEARCH_URL, CHAPTERS_LIST_URL, PAGES_LIST_URL, USER_AGENT
from mangasproject.series import Series, Category, Chapter
from mangasproject.cmdline import print_chapters


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
        resp = request('post', SEARCH_URL, json=data)
        if resp.status_code == 400:
            logger.warn("mangásPROJECT only works in Brazil, use a VPN.")
            exit(0)
        resp = resp.json()
    except requests.ConnectionError as e:
        logger.critical(str(e))
        logger.warn("mangásPROJECT only works in Brazil, use a VPN.")
        exit(0)

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
        resp = request('post', url, json=data)
        if resp.status_code == 400:
            logger.warn("mangásPROJECT only works in Brazil, use a VPN.")
            exit(0)
        resp = resp.json()
    except requests.ConnectionError as e:
        logger.critical(str(e))
        logger.warn("mangásPROJECT only works in Brazil, use a VPN.")
        exit(0)

    for chapter in resp["chapters"]:
        m = re.search("([0-9]+)-(.*)$", chapter["link"])

        c = Chapter(
            id=chapter["id_chapter"],
            id_series=chapter["id_serie"],
            series_name=chapter["name"],
            id_release=m.group(1),
            name=chapter["chapter_name"],
            number=chapter["number"],
            date=chapter["date"],
            scanlator=chapter["scanlator"],
            partner_scans=chapter["partner_scans"],
            view_count=chapter["view_count"],
            link=chapter["link"]
        )

        series.chapters.append(c)


def list_pages(chapter):
    logger.info(u"Fetching pages of {0}".format(chapter.id_release))

    data = {"id_release": chapter.id_release}
    try:
        resp = request('post', PAGES_LIST_URL, json=data)
        if resp.status_code == 400:
            logger.warn("mangásPROJECT only works in Brazil, use a VPN.")
            exit(0)
        resp = resp.json()
    except requests.ConnectionError as e:
        logger.critical(str(e))
        logger.warn("mangásPROJECT only works in Brazil, use a VPN.")
        exit(0)

    chapter.pages = resp["images"]


if __name__ == "__main__":
    series = search("One Piece")[0]
    series.show()
    list_chapters(series)
    print_chapters(series.chapters)