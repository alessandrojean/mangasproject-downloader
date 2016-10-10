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
        downloader = Downloader(timeout=options.timeout)
        for chapter in chapter_list:
            downloader.download(chapter)

    logger.info("All done.")


def signal_handler(signal, frame):
    logger.error('Ctrl-C signal received. Quit.')
    exit(1)


signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    main()
