# coding: utf-8

import sys
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
    parser = OptionParser(usage="Usage: mangasproject [options]")
    parser.add_option("--search", type="string", dest="search", action="store", help="query searched")
    parser.add_option('--page', type='int', dest='page', action='store', default=1, help='page number of list')
    parser.add_option('--id', type='int', dest='id', action='store', help=u'series id of mangásPROJECT')
    parser.add_option('--chapters', type='str', dest='chapters', action='store',
                      help='chapter numbers set, e.g. 123,987,456')
    parser.add_option('--list-chapters', dest='list_chapters', default=False, action='store_true',
                      help='list chapters of the series')
    parser.add_option('--releases', dest='releases', default=False, action='store_true', help='show last releases')
    parser.add_option('--most-read', dest='most_read', default=False, action='store_true', help='show most read series')
    parser.add_option('--most-read-period', dest='most_read_period', default=False, action='store_true',
                      help='show most read by period chapters')
    parser.add_option('--period', type='string', dest='period', action='store', default='week',
                      help='period of most read')
    parser.add_option('--adult-content', type='choice', dest='adult_content', action='store',
                      choices=[0, 1, 2], help='show adult content in most read [0, 1 or 2]')
    parser.add_option('--download', dest='is_download', action='store_true', help='download chapters or not')
    parser.add_option('--timeout', type='int', dest='timeout', action='store', default=30,
                      help='timeout of download chapter')
    parser.add_option('--disable-webp', dest='webp', action='store_false', default=True,
                      help='disable download pages as webp')

    (options, args) = parser.parse_args()

    if options.chapters:
        options.chapters = hyphen_range(options.chapters)

    if options.is_download and not options.id and not options.chapters:
        logger.critical('Chapter(s) number(s) is(are) required for downloading')
        parser.print_help()
        exit(0)

    if options.list_chapters and not options.id:
        logger.critical('Series id is required for list chapters')
        parser.print_help()
        exit(0)

    return options


def hyphen_range(x):
    result = []
    for part in x.split(','):
        if '-' in part:
            a, b = part.split('-')
            a, b = int(a), int(b)
            result.extend(range(a, b + 1))
        else:
            a = int(part)
            result.append(a)
    return result


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
        [i.id_release, i.number, i.name if i.name else '{0} #{1}'.format(i.series.name, i.number), i.scanlator, i.date]
        for i in chapters_list]
    headers = ["id", "number", "name", "scanlator", "date"]
    logger.info(u"List of chapters\n{0}".format(tabulate(
        tabular_data=chapters_list, headers=headers, tablefmt="rst"
    )))


def print_releases(releases_list):
    if not releases_list:
        return
    releases_list = [
        [i.date, i.series.id, i.series.name, i.range] for i in releases_list
    ]
    headers = ["date", "series id", "name", "chapters"]
    logger.info(u"List of last releases\n{}".format(tabulate(
        tabular_data=releases_list, headers=headers, tablefmt="rst"
    )))


def print_most_read(most_read_list):
    if not most_read_list:
        return
    most_read_list = [
        [i.id, i.name, i.view_count] for i in most_read_list
    ]
    headers = ["id", "name", "view count"];
    logger.info(u"Most read list\n{}".format(tabulate(
        tabular_data=most_read_list, headers=headers, tablefmt="rst"
    )))


def print_most_read_period(most_read_period_list):
    if not most_read_period_list:
        return
    most_read_period_list = [
        [i.id_release, "{0} #{1}".format(i.series.name, i.number), i.scanlator, i.date]
        for i in most_read_period_list
    ]
    headers = ["id", "chapter", "scanlator", "date"]
    logger.info(u"Most read by period list\n{}".format(tabulate(
        tabular_data=most_read_period_list, headers=headers, tablefmt="rst"
    )))


# Print iterations progress
def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    format_str = "{0:." + str(decimals) + "f}"
    percents = format_str.format(100 * (iteration / float(total)))
    filled_lenght = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_lenght + '-' * (bar_length - filled_lenght)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()