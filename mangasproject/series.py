from tabulate import tabulate
from mangasproject.logger import logger


class Series(object):
    def __init__(self, id, name=None, label=None, score=None, value=None, author=None, artist=None, categories=[],
                 cover=None, link=None, is_complete=False, chapters=[]):
        self.id = id
        self.name = name
        self.label = label
        self.score = score
        self.value = value
        self.author = author
        self.artist = artist
        self.categories = categories
        self.cover = cover
        self.link = link
        self.is_complete = is_complete
        self.chapters = chapters

    def __repr__(self):
        return "<Series: {0}>".format(self.name)

    def show(self):
        table = [
            ["Id", self.id],
            ["Name", self.name],
            ["Score", self.score],
            ["Author", self.author],
            ["Artist", self.artist],
            ["Complete", self.is_complete]
        ]
        logger.info(u"Print series information\n{0}".format(tabulate(table)))


class Category(object):
    def __init__(self, id, id_sub_domain=None, domain=None, name=None):
        self.id = id
        self.id_sub_domain = id_sub_domain
        self.domain = domain
        self.name = name

    def __repr__(self):
        return "<Category: {0}>".format(self.name)

    def show(self):
        table = [
            ["Id", self.id],
            ["Id Sub-Domain", self.id_sub_domain],
            ["Domain", self.domain],
            ["Name", self.name]
        ]
        logger.info(u"Print category information\n{0}".format(tabulate(table)))


class Chapter(object):
    def __init__(self, id, id_series=None, id_release=None, series_name=None, name=None, number=None, date=None,
                 scanlator=None, partner_scans=None, view_count=None, link=None, pages=[]):
        self.id = id
        self.id_series = id_series
        self.id_release = id_release
        self.series_name = series_name
        self.name = name
        self.number = number
        self.date = date
        self.scanlator = scanlator
        self.partner_scans = partner_scans
        self.view_count = view_count
        self.link = link
        self.pages = pages

    def __repr__(self):
        return "<Chapter: {0}-{1}>".format(self.number, self.name)

    def show(self):
        table = [
            ["Id", self.id],
            ["Series", self.series_name],
            ["Name", self.name],
            ["Number", self.number],
            ["Date", self.date],
            ["Scanlator", self.scanlator],
            ["Partner Scans", self.partner_scans],
            ["View Count", self.view_count]
        ]
        logger.info(u"Print chapter information\n{0}".format(tabulate(table)))


if __name__ == "__main__":
    test = Series(1, name="Naruto", categories=[Category(1, name="Action")])
    print(test)
    test.show()
    print(test.categories[0])
    test.categories[0].show()
