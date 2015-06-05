import xml
from xml.dom import minidom
from CI import CI
from mylib.string_op import *
import mylib.checking as checking

class CI_list:
    def __init__(self, list_of_ci = None):
        assert(not(list_of_ci) or checking.is_all_instance(list_of_ci, CI))

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
                date = self.get_element(ci_node, "date")
                ci = CI(name, url, date)
                self.append(ci)

        self.load_children(doc)

    def load_children(self, doc):
        for ci_node in doc.documentElement.getElementsByTagName("CI"):
            ci_name = ci_node.getElementsByTagName("name")[0].firstChild.nodeValue
            ci = self.find(ci_name)
            children_node = ci_node.getElementsByTagName("children")[0]
            for child in children_node.getElementsByTagName("child"):
                if(child.firstChild == None):
                    raise ValueError("void child balise in '" + ci_name + "'")
                else:
                    child_name = child.firstChild.nodeValue
                child_ci = self.find(child_name)
                if(child_ci != None):
                    ci.add_child(child_ci)
                else:
                    raise ValueError("try to add the child : '"+child_name+"' to '"+ci_name+"' but the child was not found")

    @classmethod
    def get_element(cls, ci_node, element):
        node = ci_node.getElementsByTagName(element)[0]

        if(node.firstChild == None):
            return None
        else:
            return node.firstChild.nodeValue

        if(element == "name"):
            return element_value
        elif(element == "url"):
            return element_value
        elif(element == "date"):
            if(element_value == ""):
                return None
            else:
                return element_value
        else:
            raise ValueError("element should be in {name, url} " + element + " given.")

    def sorted_by_name(self):
        return sorted(self.list_of_ci, key = lambda ci:ci.get_name())

    def sorted_by_date(self):
        def compare(ci):
            if(ci.get_date() != None):
                return (ci.get_date(), ci.get_name())
            else:
                return ("", ci.get_name())

        return sorted(self.list_of_ci, key = compare)

    def to_html_list(self, order="by_name"):
        string = "<html>\n"
        string += "  <head>\n"
        string += '    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />'
        string += "  </head>\n"
        string += "  <body>\n"
        string += "    <ul>\n"

        if(order == "by_name"):
            sorted_list_of_ci = self.sorted_by_name()
        elif(order == "by_date"):
            sorted_list_of_ci = self.sorted_by_date()
        else:
            raise ValueError("order should be 'by_name', or 'by_date'. '"+order+"' given.")

        if((order == "by_date")and(len(sorted_list_of_ci) > 0)):
            date = sorted_list_of_ci[0].get_date()
            if(date != None):
                str_date = date
            else:
                str_date = "unknown"
            string += '      <h2>'+str_date+'</h2>'

        for ci in sorted_list_of_ci:
            if((order == "by_date")and(ci.get_date() != date)):
                date = ci.get_date()
                if(date != None):
                    str_date = date
                else:
                    str_date = "unknown"

                string += '      <h2>'+str_date+'</h2>'

            string += '      <li><a href="' + ci.get_url() + '">' + ci.get_name() + '</a></li>\n'

        string += "    </ul>\n"
        string += "  </body>\n"
        string += "</html>\n"

        return string

    def to_graphviz(self, translate = None):
        if(translate == None):
            translate = lambda x:x

        string = "digraph CI {\n"
        string += '    node [fontcolor=blue, fontsize=8];\n'
        for ci in self:
            string += '    "' + translate(ci.get_name()) + '"[URL="'+ci.url+ '"];\n'
            for child in ci.get_children():
                string +='    "' + translate(ci.get_name()) + '"->"' + child.get_name() + '";\n'
        string += "}"

        return replace_special_char(string)
