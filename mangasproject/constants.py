VERSION = "1.0"

USER_AGENT = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36"
URL = "https://mangas.zlx.com.br"

SEARCH_URL = "%s/lib/search/series.json" % URL
CHAPTERS_LIST_URL = "%s/series/chapters_list.json?page=" % URL
PAGES_LIST_URL = "%s/leitor/pages.json" % URL
SCANLATORS_URL = "%s/scanlators/scanlators_list.json" % URL
CATEGORIES_URL = "%s/categories/categories_list.json" % URL
CATEGORIES_SERIES_URL = "%s/categories/categories_series_list.json" % URL
SERIES_URL = "%s/series/series_list.json?page=" % URL