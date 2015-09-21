"""
See CentreOfInterest(CI) class.
"""

class CentreOfInterest:
    """ A centre of interest(CI), linked to the algosphere alliance or to one of his CI"""
    def __init__(self, name, url="", date=None, children=None, translations=None):
        self._name = name
        self._url = url
        self._date = date

        # ci which are more specific than this ci
        if children == None:
            self._children = []
        else:
            self._children = children

        if translations == None:
            self._translations = {}
        else:
            self._translations = translations

    def __str__(self):
        tmp = "-"*10 + "CI" + "-"*10 + "\n"
        tmp += "name : " + str(self.name) + "\n"
        tmp += "url : " + str(self.url) + "\n"
        return tmp

    def add_child(self, child):
        """ add a child CI """
        assert isinstance(child, CentreOfInterest)
        self._children.append(child)

    @property
    def children(self):
        """ get all the child CI of this CI """
        return self._children

    def add_translation(self, lang, translation):
        """ add a translation of the name of the CI in the language 'lang'"""
        assert isinstance(lang, str)
        assert isinstance(translation, str)
        self._translations[lang] = translation

    @property
    def translations(self):
        """ get all translation """
        return self._translations

    def translate(self, lang):
        """ translate the name of the CI in langage 'lang' """
        assert isinstance(lang, str)
        if lang in self._translations:
            return self._translations[lang]
        else:
            return None

    @property
    def date(self):
        """ Date of the CI connection to the algosphere alliance """
        return self._date

    @date.setter
    def date(self, date):
        """ See date property """
        self._date = date

    @property
    def name(self):
        """ Name of the CI """
        return self._name

    @name.setter
    def name(self, name):
        """ see get_name """
        self._name = name

    @property
    def url(self):
        """ Url of the CI """
        return self._url

    @url.setter
    def url(self, url):
        """ see get_url """
        self._url = url
