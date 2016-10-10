from tabulate import tabulate
from mangasproject.logger import logger


class Series(object):
    def __init__(self, id=None, name=None, label=None, score=None, value=None, author=None, artist=None, categories=[],
                 cover=None, link=None, is_complete=False, chapters=[], view_count=None):
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
        self.view_count = view_count

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
    def __init__(self, id=None, id_release=None, name=None, number=None, date=None,
                 scanlator=None, partner_scans=None, view_count=None, link=None, pages=[], adult_content=False,
                 domain=None, series=Series()):
        self.id = id
        self.id_release = id_release
        self.name=name
        self.number = number
        self.date = date
        self.scanlator = scanlator
        self.partner_scans = partner_scans
        self.view_count = view_count
        self.link = link
        self.pages = pages
        self.adult_content = adult_content
        self.domain = domain
        self.series = series

    def __repr__(self):
        return "<Chapter: {0}-{1}>".format(self.number, self.series.name)

    def show(self):
        table = [
            ["Id", self.id],
            ["Series", self.series.name],
            ["Name", self.name],
            ["Number", self.number],
            ["Date", self.date],
            ["Scanlator", self.scanlator],
            ["Partner Scans", self.partner_scans],
            ["View Count", self.view_count]
        ]
        logger.info(u"Print chapter information\n{0}".format(tabulate(table)))


class Release(object):
    def __init__(self, date=None, date_created=None, series=None, range=None, chapters=None):
        self.date = date
        self.date_created = date_created
        self.series = series
        self.range = range
        self.chapters = chapters

    def __repr__(self):
        return "<Release: {0} {1}>".format(self.series.name, self.range)

    def show(self):
        table = [
            ["Date", self.date],
            ["Date Created", self.date_created],
            ["Series", self.series.name],
            ["Range", self.range]
        ]
        logger.info(u"Print release information\n{}".format(tabulate(table)))


if __name__ == "__main__":
    test = Series(1, name="Naruto", categories=[Category(1, name="Action")])
    print(test)
    test.show()
    print(test.categories[0])
    test.categories[0].show()
