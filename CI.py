#!/bin/python

class CI:
    """center of interest"""
    def __init__(self, name, url="", children=[], translations=[]):
        self.name = name
        self.url = url
        # ci the are more specific than this ci
        self.children = children
        self.translations = translations

    def __str__(self):
        tmp = "-"*10 + "CI" + "-"*10 + "\n"
        tmp += "name : " + str(self.name) + "\n"
        tmp += "url : " + str(self.url) + "\n"
        return tmp

    def add_child(child):
        assert(isinstance(child, CI))
        self.children.add(child)

    def get_children():
        return self.children

    def add_translation(lang, translation):
        assert(type(lang) == "string")
        assert(type(lang) == "string")
        self.translations[lang] = translation

    def get_name():
        return self.name

    def set_name(name):
        self.name = name

    def get_url():
        return self.url

    def set_url(url):
        self.url = url
