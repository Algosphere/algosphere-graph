#!/bin/python

import xml
from xml.dom import minidom
from CI import CI
from mylib.string_op import *
import mylib.checking as checking

class CI_list:
    def __init__(self, list_of_ci = None):
        assert(checking.is_all_instance(list_of_ci, CI))

        if(list_of_ci == None):
            self.list_of_ci = []
        else:
            self.list_of_ci = list_of_ci

    def __iter__(self):
        for ci in self.list_of_ci:
            yield ci

    def __len__(self):
        return len(self.list_of_ci)

    def get_list_of_ci(self):
        return self.list_of_ci

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
        self.list_of_ci = []
        doc = minidom.parse(xml_file)
        for ci_node in doc.documentElement.getElementsByTagName("CI"):
                name = self.get_element(ci_node, "name")
                url = self.get_element(ci_node, "url")
                ci = CI(name, url)
                self.append(ci)

        self.load_children(doc)

    def load_children(self, doc):
        for ci_node in doc.documentElement.getElementsByTagName("CI"):
            ci_name = ci_node.getElementsByTagName("name")[0].firstChild.nodeValue
            ci = self.find(ci_name)
            children_node = ci_node.getElementsByTagName("children")[0]
            for child in children_node.getElementsByTagName("child"):
                child_name = child.firstChild.nodeValue
                child_ci = self.find(child_name)
                ci.add_child(child_ci)

    @classmethod
    def get_element(cls, ci_node, element):
        node = ci_node.getElementsByTagName(element)[0]

        if(node.firstChild == None):
            return ""
        else:
            return node.firstChild.nodeValue

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
