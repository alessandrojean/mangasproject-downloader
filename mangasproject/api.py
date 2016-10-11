# coding: utf-8
import requests
import re

from mangasproject.logger import logger
from mangasproject.constants import *
from mangasproject.model import *
from mangasproject.cmdline import print_chapters


def request(method, url, referer=URL, user_agent=USER_AGENT, **kwargs):
    if not hasattr(requests, method):
        raise AttributeError('\'requests\' object has no attribute \'{0}\''.format(method))

    headers = {"X-Requested-With": "XMLHttpRequest", "User-Agent": user_agent, "Referer": referer}
    return requests.__dict__[method](url, headers=headers, **kwargs)


def search(query):
    results = []
    logger.info(u"Searching for {0}".format(query))

    data = {"search": query}
    try:
        resp = request('post', SEARCH_URL, json=data)
    except requests.ConnectionError as e:
        logger.error(str(e))
        exit(0)

    try:
        resp = resp.json()
    except Exception as e:
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
        resp = request('post', url, referer=series.link, json=data)
    except requests.ConnectionError as e:
        logger.error(str(e))
        exit(0)

    try:
        resp = resp.json()
    except Exception as e:
        logger.warn("mangásPROJECT only works in Brazil, use a VPN.")
        exit(0)

    for chapter in resp["chapters"]:
        m = re.search("([0-9]+)-(.*)$", chapter["link"])

        s = Series(
            id=chapter["id_serie"],
            name=chapter["name"],
        )

        c = Chapter(
            id=chapter["id_chapter"],
            id_release=m.group(1),
            name=chapter["chapter_name"],
            number=chapter["number"],
            date=chapter["date"],
            scanlator=chapter["scanlator"],
            partner_scans=chapter["partner_scans"],
            view_count=chapter["view_count"],
            link=chapter["link"],
            series=s
        )

        series.chapters.append(c)


def list_pages(chapter, webp=True):
    logger.info(u"Fetching pages of {0}".format(chapter.id_release))

    data = {"id_release": chapter.id_release}
    user_agent = USER_AGENT if webp else USER_AGENT_OLD

    try:
        resp = request('post', PAGES_LIST_URL, referer=chapter.link, user_agent=user_agent, json=data)
    except requests.ConnectionError as e:
        logger.error(str(e))
        exit(0)

    try:
        resp = resp.json()
    except Exception as e:
        logger.warn("mangásPROJECT only works in Brazil, use a VPN.")
        exit(0)

    chapter.pages = resp["images"]


def list_releases(page=1):
    results = []
    logger.info(u"Fetching releases")

    url = "{0}{1}".format(RELEASES_URL, page)
    try:
        resp = request('get', url)
    except requests.ConnectionError as e:
        logger.error(str(e))
        exit(0)

    try:
        resp = resp.json()
    except Exception as e:
        logger.warn("mangásPROJECT only works in Brazil, use a VPN.")
        exit(0)

    for release in resp["releases"]:
        s = Series(
            id=release["id_serie"],
            name=release["name"],
            cover=release["image"],
            link="{0}{1}".format(URL, release["link"])
        )

        ch = []
        for chapter in release["chapters"]:
            m = re.search("([0-9]+)-(.*)$", chapter["url"])

            c = Chapter(
                link=chapter["url"],
                number=chapter["number"],
                id_release=m.group(1)
            )
            ch.append(c)

        r = Release(
            date=release["date"],
            date_created=release["date_created"],
            series=s,
            range=release["range"],
            chapters=ch
        )

        results.append(r)

    return results


def list_most_read(page=1):
    results = []
    logger.info(u"Fetching most read list")

    url = "{0}{1}".format(MOST_READ_URL, page)
    try:
        resp = request('get', url)
    except requests.ConnectionError as e:
        logger.error(str(e))
        exit(0)

    try:
        resp = resp.json()
    except Exception as e:
        logger.warn("mangásPROJECT only works in Brazil, use a VPN.")
        exit(0)

    for series in resp["most_read"]:
        s = Series(
            id=series["id_serie"],
            name=series["serie_name"],
            cover=series["cover"],
            link="{0}{1}".format(URL, series["link"]),
            view_count=series["view_count"]
        )

        results.append(s)

    return results


def list_most_read_period(period='week', adult_content=0):
    results = []
    logger.info(u"Fetching most read by {} list".format(period))
    if adult_content > 0:
        logger.info("Showing {}adult content".format("only " if adult_content == 2 else ""))

    data = {"period": period, "adult_content": adult_content}
    try:
        resp = request('post', MOST_READ_PERIOD_URL, json=data)
    except requests.ConnectionError as e:
        logger.error(str(e))
        exit(0)

    try:
        resp = resp.json()
    except Exception as e:
        logger.warn("mangásPROJECT only works in Brazil, use a VPN.")
        exit(0)

    for chapter in resp["most_read"]:
        s = Series(
            id=chapter["id_serie"],
            cover=chapter["series_image"],
            name=chapter["series_name"],
            link=chapter["serie_link"]
        )

        c = Chapter(
            adult_content=chapter["adult_content"],
            id_release=chapter["id_release"],
            domain=chapter["domain"],
            number=chapter["chapter_number"],
            scanlator=chapter["scanlator"],
            date=chapter["date"],
            link=chapter["link"],
            series=s
        )

        results.append(c)

    return results


if __name__ == "__main__":
    series = search("One Piece")[0]
    series.show()
    list_chapters(series)
    print_chapters(series.chapters)