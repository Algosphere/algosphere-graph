"""
See CentreOfInterest(CI) class.
"""

class CentreOfInterest:
    """ A centre of interest(CI), linked to the algosphere alliance or to one of his CI"""
    def __init__(self, name, url="", date=None, children=None, translations=None):
        self.name = name
        self.url = url
        self.date = date # connection date of the CI

        # ci which are more specific than this ci
        if children == None:
            self.children = []
        else:
            self.children = children

        if translations == None:
            self.translations = {}
        else:
            self.translations = translations

    def __str__(self):
        tmp = "-"*10 + "CI" + "-"*10 + "\n"
        tmp += "name : " + str(self.name) + "\n"
        tmp += "url : " + str(self.url) + "\n"
        return tmp

    def add_child(self, child):
        """ add a child CI """
        assert isinstance(child, CentreOfInterest)
        self.children.append(child)

    def get_children(self):
        """ get all the child CI of this CI """
        return self.children

    def add_translation(self, lang, translation):
        """ add a translation of the name of the CI in the language 'lang'"""
        assert isinstance(lang, str)
        assert isinstance(translation, str)
        self.translations[lang] = translation

    def get_translations(self):
        """ get all translation """
        return self.translations

    def translate(self, lang):
        """ translate the name of the CI in langage 'lang' """
        assert isinstance(lang, str)
        if lang in self.translations:
            return self.translations[lang]
        else:
            return None

    def get_date(self):
        """ get the date when the CI have be had """
        return self.date

    def set_date(self, date):
        """ see get_date """
        self.date = date

    def get_name(self):
        """ get the name of the CI """
        return self.name

    def set_name(self, name):
        """ see get_name """
        self.name = name

    def get_url(self):
        """ get the url of the CI """
        return self.url

    def set_url(self, url):
        """ see get_url """
        self.url = url
