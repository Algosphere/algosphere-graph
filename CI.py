#!/bin/python

class CI:
    """center of interest"""
    def __init__(self, name, url="", children=None, translations=None):
        self.name = name
        self.url = url
        # ci the are more specific than this ci
        if(children == None):
            self.children = []
        else:
            self.children = children

        if(translations == None):
            self.translations = {}
        else:
            self.translations = translations

    def __str__(self):
        tmp = "-"*10 + "CI" + "-"*10 + "\n"
        tmp += "name : " + str(self.name) + "\n"
        tmp += "url : " + str(self.url) + "\n"
        return tmp

    def add_child(self, child):
        assert(isinstance(child, CI))
        self.children.append(child)

    def get_children(self):
        return self.children

    def add_translation(self, lang, translation):
        assert(isinstance(lang, str))
        assert(isinstance(translation, str))
        self.translations[lang] = translation

    def get_translations(self):
        return self.translations

    def translate(self, lang):
        assert(isinstance(lang, str))
        if(lang in self.translations):
            return self.translations[lang]
        else:
            return None

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url
