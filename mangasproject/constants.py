VERSION = "1.0"

USER_AGENT = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36"
USER_AGENT_OLD = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
URL = "https://mangas.zlx.com.br"

SEARCH_URL = "%s/lib/search/series.json" % URL
CHAPTERS_LIST_URL = "%s/series/chapters_list.json?page=" % URL
PAGES_LIST_URL = "%s/leitor/pages.json" % URL
SCANLATORS_URL = "%s/scanlators/scanlators_list.json" % URL
SCANLATORS_SERIES_URL = "%s/scanlators/series_list.json?page=" % URL
CATEGORIES_URL = "%s/categories/categories_list.json" % URL
CATEGORIES_SERIES_URL = "%s/categories/series_list.json?page=" % URL
SERIES_URL = "%s/series/series_list.json?page=" % URL
RELEASES_URL = "%s/home/releases.json?page=" % URL
MOST_READ_URL = "%s/home/most_read.json?page=" % URL
MOST_READ_PERIOD_URL = "%s/home/most_read_period.json" % URL

CHOICES = [
    'all',
    'best_scores',
    'most_read',
    'recently_updated',
    'chapters_number',
    'recently_completed',
    'favorites'
]

CHOICES_NAME = [
    'All (A-Z)',
    'Best scores',
    'Most read',
    'Recently updated',
    'Chapters number',
    'Recently completed',
    'Favorites'
]
