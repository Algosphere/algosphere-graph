"""
See CentresOfInterestManager class
"""

import re
import mylib.checking as checking
from mylib.string_op import replace_special_char
from mylib.notifier import Notifier
from xml.dom import minidom
from lxml import etree
from centre_of_interest import CentreOfInterest

def identity(x):
    return x

class CentresOfInterestManager:
    """
    Class that permit to create/load lists of ci(center of interest),
    and to export them in different formats.
    """
    def __init__(self, list_of_ci=None, notifier=None):
        assert not(list_of_ci) or\
            checking.is_all_instance(list_of_ci, CentreOfInterest)

        self.ci_dtd = "ci.dtd"
        self.ci_graph_dtd = "ci_graph.dtd"

        # Templates html tags
        self.html_start_list = "<ul>\n"
        self.html_end_list = "</ul>\n"
        self.html_date = "<h2>{date}</h2>\n"
        self.html_item = '<li><a href="{url}">{name}</a></li>\n'

        # Templates graphviz tags
        self.dot_start_graph = "digraph CI {\n" +\
                               "    node [fontcolor=red, fontsize=8];\n"
        self.dot_end_graph = "}"
        self.dot_official_item = '  "{name_official}"[URL="{url}", style=filled, fillcolor="0 0 0"];\n'
        self.dot_unofficial_item = '  "{name_unofficial}"[URL="{url}", style=filled, fillcolor="0 0 0"];\n'
        self.dot_without_url_item = '  "{name_without_url}"[style=filled, fillcolor="0 0 0"];\n'
        self.dot_item_child = '  "{name_official}"->"{child}";\n'
        if notifier is not None:
            assert isinstance(notifier, Notifier)

        self._only_official = False
        self._notifier = notifier
        if list_of_ci is None:
            self._list_of_ci = []
        else:
            self._list_of_ci = list_of_ci

    def notify(self, text):
        """
        notify something to the user (use the Notifier object)
        """
        if self._notifier is not None:
            self._notifier.notify(text)

    def __iter__(self):
        for centre_of_interest in self._list_of_ci:
            yield centre_of_interest

    def __len__(self):
        return len(self._list_of_ci)

    @property
    def list_of_ci(self):
        """ get the list of ci managed """
        return self._list_of_ci

    def append(self, centre_of_interest):
        """ add a new centre of interest to be managed """
        assert isinstance(centre_of_interest, CentreOfInterest)
        self._list_of_ci.append(centre_of_interest)

    def __str__(self):
        tmp = ""
        for centre_of_interest in self._list_of_ci:
            tmp += str(centre_of_interest)
        return tmp

    def find(self, ci_name):
        """ find a centre of interest by name """
        assert isinstance(ci_name, str)
        for centre_of_interest in self:
            if centre_of_interest.name == ci_name:
                return centre_of_interest
        return None

    def verify_xml(self, xml_file_path, dtd_file_path):
        with open(dtd_file_path, 'r', encoding='utf-8') as dtd_file:
            with open(xml_file_path, 'r', encoding='utf-8') as xml_file:
                dtd = etree.DTD(dtd_file)
                root = etree.parse(xml_file)
                if not dtd.validate(root):
                    raise IOError('Not valide according to "' + dtd_file_path +
                                  '"\n' +
                                  str(dtd.error_log.filter_from_errors()[0]))

    def delete_unwanted_ci(self):
        if self._only_official:
            self._list_of_ci = [ci for ci in self._list_of_ci if ci.official]
            for ci in self._list_of_ci:
                ci.children = [child for child in ci.children if child.official]

    def load_xml(self, xml_file, only_official=False, with_link=True):
        """ load all the centres of interest from a xml file """
        self.notify('load xml_file "' + xml_file + '"')
        self.verify_xml(xml_file, self.ci_dtd)
        self._list_of_ci = []
        self._only_official = only_official
        doc = minidom.parse(xml_file)
        for ci_node in doc.documentElement.getElementsByTagName("CI"):
            name = self._get_element(ci_node, "name")
            if with_link:
                #url == None, if the <url> balise is empty
                url = self._get_element(ci_node, "url")
            else:
                url = ''
            date = self._get_element(ci_node, "date")
            official = self._get_element(ci_node, "official")
            centre_of_interest = CentreOfInterest(name, url, date)
            centre_of_interest.official = official
            self.append(centre_of_interest)

    def load_children(self, ci_graph_file):
        """
        Make the link between the centres of interest and their children
        """
        self.verify_xml(ci_graph_file, self.ci_graph_dtd)
        doc = minidom.parse(ci_graph_file)

        for ci_node in doc.documentElement.getElementsByTagName("CI"):
            ci_name = ci_node.getElementsByTagName("name")[0].firstChild.nodeValue
            centre_of_interest = self.find(ci_name)
            if centre_of_interest is None:
                raise ValueError('"' + ci_name + '" found in "' +
                                 ci_graph_file + '" doesn\'t exist in ci.xml')
            children_node = ci_node.getElementsByTagName("children")[0]
            child_nodes = children_node.getElementsByTagName("child")

            for child in child_nodes:
                if child.firstChild is None:
                    raise ValueError("void child balise in '" + ci_name + "'")
                else:
                    child_name = child.firstChild.nodeValue
                child_ci = self.find(child_name)

                if child_ci is not None:
                    centre_of_interest.add_child(child_ci)
                else:
                    raise ValueError("try to add the child : '" +
                                     child_name +
                                     "' to '" +
                                     ci_name +
                                     "' but the child was not found")

    @classmethod
    def _get_element(cls, ci_node, element):
        """
        Get the element 'element', of the centre of interest node 'ci_node'
        """
        node = ci_node.getElementsByTagName(element)[0]

        if node.firstChild is None:
            return None
        else:
            return node.firstChild.nodeValue

    def sorted_by_name(self, translate=None):
        """
        Return the list of CI sorted by name.

        :param translate: a function used to translate the CI name,
        translate(ci_name)=ci_name_translated

        :type translate: function
        """
        if translate is not None:
            return sorted(self._list_of_ci, key=lambda ci: translate(ci.name))
        else:
            return sorted(self._list_of_ci, key=lambda ci: ci.name)

    def sorted_by_date(self, translate=None):
        """
        Return the list of CI sorted by date.

        :param translate: a function used to translate the CI name,
        translate(ci_name)=ci_name_translated

        :type translate: function
        """

        if translate is None:
            translate = identity

        def get_date_name(centre_of_interest):
            """ return a couple (ci_date, ci_name), to sort the list """
            if centre_of_interest.date is not None:
                return (centre_of_interest.date,
                        translate(centre_of_interest.name))
            else:
                return ("", translate(centre_of_interest.name))

        return sorted(self._list_of_ci, key=get_date_name)

    def load_template_dot(self, dot_file_path):
        self.notify('load dot template file "' + dot_file_path + '"')
        def get_match(match, message):
            if not match:
                raise IOError(message)
            else:
                return match.group(1)

        with open(dot_file_path, 'r', encoding='utf-8') as dot_file:
            template = dot_file.read()
            start_graph = re.search(r'^(.*)// official ci start',
                                    template,
                                    re.DOTALL)
            self.dot_start_graph = get_match(start_graph,
                                             "Incorrect dot template, can’t find start")

            end_graph = re.search(r'// child end(.*)$', template, re.DOTALL)
            self.dot_end_graph = get_match(end_graph, "Incorrect dot template, can’t find end")


            official_item = re.search(r'// official ci start(.*)// official ci end',
                                      template,
                                      re.DOTALL)
            self.dot_official_item = get_match(official_item,
                                               "Incorrect dot template, can’t find official ci item")

            unofficial_item = re.search(r'// unofficial ci start(.*)// unofficial ci end',
                                        template,
                                        re.DOTALL)
            self.dot_unofficial_item = get_match(unofficial_item,
                                                 "Incorrect dot template, can’t find unofficial ci item")

            without_url_item = re.search(r'// without_url start(.*)// without_url end',
                                         template,
                                         re.DOTALL)
            self.dot_without_url_item = get_match(without_url_item,
                                                  "Incorrect dot template, can’t find without url ci item")

            item_child = re.search(r'// child start(.*)// child end',
                                   template,
                                   re.DOTALL)

            self.dot_item_child = get_match(item_child,
                                            "Incorrect dot template, can’t find child ci item")

    def load_template_html(self, html_file_path):
        self.notify('load html template file "' + html_file_path + '"')

        with open(html_file_path, 'r', encoding='utf-8') as html_file:
            template = html_file.read()
            start_list = re.search(r'^(.*)<!-- date -->', template, re.DOTALL)
            if not start_list:
                raise IOError("Incorrect html template, can’t find start")
            else:
                self.html_start_list = start_list.group(1)

            end_list = re.search(r'<!-- /item -->(.*)$', template, re.DOTALL)
            if not end_list:
                raise IOError("Incorrect html template, can’t find end")
            else:
                self.html_end_list = end_list.group(1)

            date = re.search(r'<!-- date -->(.*)<!-- /date -->',
                             template,
                             re.DOTALL)
            if not date:
                raise IOError("Incorrect html template, can’t find date")
            else:
                self.html_date = date.group(1)

            item = re.search(r'<!-- item -->(.*)<!-- /item -->',
                             template,
                             re.DOTALL)
            if not item:
                raise IOError("Incorrect html template, can’t find item")
            else:
                self.html_item = item.group(1)

    def to_html_list(self, order="by_name", translate=None):
        """
        Export the sorted list of CI to html.

        :param order: choose "by_name" to sort by name and "by_date" to sort by date
        :param translate: a function used to translate the CI name,
        translate(ci_name)=ci_name_translated
        :type order: str
        :type translate: function
        :return: return a string corresponding of the html page
        """

        self.delete_unwanted_ci()
        if translate is None:
            translate = identity

        string = self.html_start_list

        if order == "by_name":
            sorted_list_of_ci = self.sorted_by_name(translate)
        elif order == "by_date":
            sorted_list_of_ci = self.sorted_by_date(translate)
        else:
            raise ValueError("order should be 'by_name', or 'by_date'. '" +
                             order +
                             "' given.")

        if (order == "by_date")and(len(sorted_list_of_ci) > 0):
            date = sorted_list_of_ci[0].date
            if date is not None:
                str_date = date
            else:
                str_date = "unknown"
            string += self.html_date.replace('{date}', str_date)

        for centre_of_interest in sorted_list_of_ci:
            if (order == "by_date")and(centre_of_interest.date != date):
                date = centre_of_interest.date
                if date is not None:
                    str_date = date
                else:
                    str_date = "unknown"

                string += self.html_date.replace('{date}', str_date)
            if centre_of_interest.url is not None:
                item = self.html_item.replace('{url}', centre_of_interest.url)
                item = item.replace('{name}',
                                    translate(centre_of_interest.name))
                string += item

        string += self.html_end_list

        return string

    def to_graphviz(self, ci_graph_file, translate=None):
        """
        Export the sorted list of CI to a graphviz dot format.

        :param translate: a function used to translate the CI name,
        translate(ci_name)=ci_name_translated
        :type translate: function
        :return: return a string corresponding of the dot file
        """
        self.load_children(ci_graph_file)
        self.delete_unwanted_ci()

        if translate is None:
            translate = identity

        string = self.dot_start_graph

        for centre_of_interest in self:

            if centre_of_interest.url is None or centre_of_interest.url == '':
                dot_template = self.dot_without_url_item
            else:
                if centre_of_interest.official:
                    dot_template = self.dot_official_item
                else:
                    dot_template = self.dot_unofficial_item

            item_name = translate(centre_of_interest.name)
            item = re.sub(r'{name.*?}', item_name, dot_template)
            if centre_of_interest.url is not None:
                item = re.sub(r'{url}', centre_of_interest.url, item)
            string += item

            for child in centre_of_interest.children:
                item_child = re.sub(r'{name.*?}', item_name,
                                    self.dot_item_child)
                item_child = re.sub(r'{child}', translate(child.name),
                                    item_child)

                string += item_child

        string += self.dot_end_graph

        return replace_special_char(string)
