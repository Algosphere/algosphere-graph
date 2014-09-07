#!/bin/python

class CI:
    def __init__(self, name, url=""):
        self.name = name
        self.url = url

    def __str__(self):
        tmp = "-"*10 + "CI" + "-"*10 + "\n"
        tmp += "name : " + str(self.name) + "\n"
        tmp += "url : " + str(self.url) + "\n"
        return tmp
