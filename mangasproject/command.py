import sys
import signal

from mangasproject.cmdline import banner, cmd_parser, print_series, print_chapters
from mangasproject.api import search, list_chapters
from mangasproject.series import Series, Chapter
from mangasproject.logger import logger
from mangasproject.downloader import Downloader


def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    banner()
    options = cmd_parser()

    chapter_ids = options.ids
    chapter_list = []

    if options.search:
        results = search(options.search)
        print_series(results)

    if options.chapters:
        series = Series(options.id)
        list_chapters(series, page=options.page)
        print_chapters(series.chapters)

    if chapter_ids:
        for id in chapter_ids:
            chapter_list.append(Chapter(id=None, id_release=id,))
    else:
        exit(0)

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
