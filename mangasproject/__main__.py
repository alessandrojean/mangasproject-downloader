# coding: utf-8
import signal

from mangasproject.cmdline import *
from mangasproject.api import *
from mangasproject.model import *
from mangasproject.logger import logger
from mangasproject.downloader import Downloader


def main():
    banner()
    options = cmd_parser()

    chapter_list = []

    if options.list_series:
        if options.category_id is not None:
            results = list_categories_series(Category(id=options.category_id), options.page)
            print_series_list(results, option='category')
        elif options.scanlator_id is not None:
            results = list_scanlators_series(Scanlator(id=options.scanlator_id), options.page)
            print_series_list(results, option='scanlator')
        else:
            results = list_series(sort_by=CHOICES.index(options.sort_by), initial=options.initial,
                                  period=options.period, page=options.page)
            print_series_list(results, option=options.sort_by)

    if options.list_categories:
        results = list_categories()
        print_categories(results)

    if options.list_scanlators:
        results = list_scanlators()
        print_scanlators(results)

    if options.search:
        results = search(options.search)
        print_series(results)

    if options.releases:
        results = list_releases(options.page)
        print_releases(results)

    if options.most_read:
        results = list_most_read(options.page)
        print_most_read(results)

    if options.most_read_period:
        results = list_most_read_period(options.period, options.adult_content)
        print_most_read_period(results)

    if options.list_chapters:
        series = Series(id=options.id)
        list_chapters(series, page=options.page)
        print_chapters(series.chapters)

    if options.chapters:
        series = Series(id=options.id)
        list_chapters(series, page=options.page)

        for number in options.chapters:
            for chapter in series.chapters:
                if str(chapter.number) == str(number):
                    chapter_list.append(chapter)

        if len(chapter_list) > 0:
            print_chapters(chapter_list)
        else:
            logger.warn("Chapter(s) not found, check another page with the argument --page x")

    if options.is_download:
        if not options.webp:
            logger.info("Webp downloading disabled, turn it on if you want your chapters with smaller size.")
        downloader = Downloader(timeout=options.timeout, webp=options.webp)
        for chapter in chapter_list:
            downloader.download(chapter)

    logger.info("All done.")


def signal_handler(signal, frame):
    logger.error('Ctrl-C signal received. Quit.')
    exit(1)


signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    main()
