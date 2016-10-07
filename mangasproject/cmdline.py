# coding: utf-8

from mangasproject.logger import logger
from mangasproject import __version__
from optparse import OptionParser
from tabulate import tabulate


def banner():
    logger.info('''mangásPROJECT Downloader v{0}
                  ____                      _                 _
  _ __ ___  _ __ |  _ \  _____      ___ __ | | ___   __ _  __| | ___ _ __
 | '_ ` _ \| '_ \| | | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
 | | | | | | |_) | |_| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |
 |_| |_| |_| .__/|____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|
           |_|
'''.format(__version__))


def cmd_parser():
    parser = OptionParser()
    parser.add_option("--search", type="string", dest="search", action="store", help="query searched")
    parser.add_option('--page', type='int', dest='page', action='store', default=1, help='page number of list')
    parser.add_option('--id', type='int', dest='id', action='store', help='series/chapter id of mangasPROJECT')
    parser.add_option('--ids', type='str', dest='ids', action='store', help='chapter id set, e.g. 123,987,456')
    parser.add_option('--chapters', dest='chapters', default=False, action='store_true',
                      help='list chapters of the series')
    parser.add_option('--download', dest='is_download', action='store_true', help='download chapters or not')
    parser.add_option('--timeout', type='int', dest='timeout', action='store', default=30,
                      help='timeout of download chapter')

    (options, args) = parser.parse_args()

    if options.ids:
        args = map(lambda id: id.strip(), options.ids.split(','))
        options.ids = set(map(int, filter(lambda id: id.isdigit(), args)))

    if options.is_download and not options.id and not options.ids:
        logger.critical('Chapter id/ids is required for downloading')
        parser.print_help()
        exit(0)

    if options.id:
        options.ids = (options.id,) if not options.ids else options.ids

    if options.chapters and not options.id:
        logger.critical('Series id is required for list chapters')
        parser.print_help()
        exit(0)

    return options


def print_series(series_list):
    if not series_list:
        return
    series_list = [[i.id, i.name] for i in series_list]
    headers = ["id", "name"]
    logger.info(u"Search result\n{0}".format(tabulate(
        tabular_data=series_list, headers=headers, tablefmt="rst"
    )))


def print_chapters(chapters_list):
    if not chapters_list:
        return
    chapters_list = [
        [i.id_release, i.number, i.name if i.name else '{0} #{1}'.format(i.series_name, i.number), i.scanlator, i.date]
        for i in chapters_list]
    headers = ["id", "number", "name", "scanlator", "date"]
    logger.info(u"List of chapters\n{0}".format(tabulate(
        tabular_data=chapters_list, headers=headers, tablefmt="rst"
    )))
