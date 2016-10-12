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
    parser.add_option('--period', type='choice', dest='period', action='store',
                      choices=['ever', 'day', 'week', 'month', 'year'], help='period')
    parser.add_option('--adult-content', type='choice', dest='adult_content', action='store',
                      choices=['0', '1', '2'], help='show adult content in most read [0, 1 or 2]')
    parser.add_option('--list-series', dest='list_series', default=False, action='store_true', help='list series')
    parser.add_option('--list-categories', dest='list_categories', default=False, action='store_true',
                      help='list categories')
    parser.add_option('--list-scanlators', dest='list_scanlators', default=False, action='store_true',
                      help='list scanlators')
    parser.add_option('--category', type='int', dest='category_id', action='store', help='category id to show series')
    parser.add_option('--scanlator', type='int', dest='scanlator_id', action='store', help='scanlator id to show series')
    parser.add_option('--sort-by', type='choice', dest='sort_by', action='store',
                      choices=[
                          'all',
                          'best_scores',
                          'most_read',
                          'recently_updated',
                          'chapters_number',
                          'recently_completed',
                          'favorites'
                      ],
                      help='sort series list by ...', default='all'
                      )
    parser.add_option('--initial', type='string', dest='initial', default='all', action='store', help='initial of series list')
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

    if options.list_series:
        if not options.initial == 'all' and not options.initial == 'nan':
            alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)]
            if options.initial not in alphabet:
                logger.critical('The initial specified it\'s not valid')
                exit(0)
        if options.period == 'week':
            logger.critical('The period specified it\'s not valid')
            exit(0)
        if options.period is None:
            options.period = 'ever'

    if options.most_read_period and options.period is None:
        options.period = 'week'

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


def print_scanlators(scanlators_list):
    if not scanlators_list:
        return
    scanlators_list = [[i.id, i.name, i.titles, i.view_count] for i in scanlators_list]
    headers = ["id", "name", "titles", "view count"]
    logger.info(u"Scanlators list\n{0}".format(tabulate(
        tabular_data=scanlators_list, headers=headers, tablefmt="rst"
    )))


def print_categories(categories_list):
    if not categories_list:
        return
    categories_list = [[i.id, i.name, i.titles, i.view_count] for i in categories_list]
    headers = ["id", "name", "titles", "view count"]
    logger.info(u"Categories list\n{0}".format(tabulate(
        tabular_data=categories_list, headers=headers, tablefmt="rst"
    )))


def print_series(series_list):
    if not series_list:
        return
    series_list = [[i.id, i.name] for i in series_list]
    headers = ["id", "name"]
    logger.info(u"Search result\n{0}".format(tabulate(
        tabular_data=series_list, headers=headers, tablefmt="rst"
    )))


def print_series_list(series_list, option='all'):
    if not series_list:
        return
    headers = []
    if option == 'category':
        headers = ["id", "name", "chapters", "score"]
        series_list = [[i.id, i.name, i.chapters_count, i.score] for i in series_list]
    elif option == 'scanlator':
        headers = ["id", "name", "releases", "date last release", "score", "view count"]
        series_list = [[i.id, i.name, i.releases_count, i.date_last_release, i.score, i.view_count] for i in series_list]
    elif option == 'all':
        headers = ["initial", "id", "name", "chapters", "score"]
        series_list = [[i.menu_tag['initial'], i.id, i.name, i.chapters_count, i.score] for i in series_list]
    elif option == 'best_scores':
        headers = ["score", "id", "name", "chapters", "score"]
        series_list = [[i.score, i.id, i.name, i.chapters_count, i.score] for i in series_list]
    elif option == 'most_read':
        headers = ["position", "id", "name", "chapters", "score"]
        series_list = [[i.menu_tag['views'], i.id, i.name, i.chapters_count, i.score] for i in series_list]
    elif option == 'recently_updated' or option == 'recently_completed':
        headers = ["date", "id", "name", "chapters", "score"]
        series_list = [[i.menu_tag['date'], i.id, i.name, i.chapters_count, i.score] for i in series_list]
    elif option == 'chapters_number':
        headers = ["chapters", "id", "name", "chapters", "score"]
        series_list = [[i.menu_tag['chapters'], i.id, i.name, i.chapters_count, i.score] for i in series_list]
    elif option == 'favorites':
        headers = ["favorites", "id", "name", "chapters", "score"]
        series_list = [[i.menu_tag['favorite_count'], i.id, i.name, i.chapters_count, i.score] for i in series_list]
    logger.info(u"Series list\n{0}".format(tabulate(
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