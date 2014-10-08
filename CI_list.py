#!/bin/python

import xml
from xml.dom import minidom
from CI import CI
from mylib.string_op import *

class CI_list:
    def __init__(self, list_of_ci):
        self.list_of_ci = list_of_ci

    def __iter__(self):
        for ci in self.list_of_ci:
            yield ci

    def append(self, ci):
        assert(isinstance(ci, CI))
        self.list_of_ci.append(ci)

    def __str__(self):
        tmp = ""
        for ci in self.list_of_ci:
            tmp += str(ci)
        return tmp

    def find(self, ci_name):
        assert(type(ci_name) == str)
        for ci in self:
            if(ci.name == ci_name):
                return ci
        return None

    def load_xml(self, xml_file):
        doc = minidom.parse(xml_file)
        for ci in doc.documentElement.childNodes:
            if(ci.nodeType == minidom.Node.ELEMENT_NODE):
                name = self.get_element(ci, "name")
                url = self.get_element(ci, "url")
                # children = self.get_element(ci, "children")
                self.append(CI(name, url))

    @classmethod
    def get_element(cls, ci_node, element):
        element_value = ci_node.getElementsByTagName(element)[0].firstChild
        if(element_value == None):
            return ""
        else:
            element_value = element_value.nodeValue

        if(element == "name"):
            return element_value
        elif(element == "url"):
            return element_value
        else:
            raise ValueError("element should be in {name, url} " + element + " given.")

    def to_graphviz(self):
        string = "digraph CI {\n"
        for ci in self:
            string += '    "' + ci.name + '";\n'
            string += "}"

        return replace_special_char(string)
