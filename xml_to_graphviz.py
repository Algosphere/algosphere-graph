#!/bin/python

"""
Create graphviz files (.dot) from a xml file describing a list of centres of interest.

Usage: see '>>xml_to_graphviz.py --help'

command line to transform ci.dot in ci.svg :
dot -Tsvg ci.dot > ci.svg
"""

import argparse

from centres_of_interest_manager import CentresOfInterestManager
from translations_manager import TranslationsManager
from mylib.notifier import Notifier

def create_graph_for_language(translations_manager,
                              ci_manager,
                              lang_file,
                              output_file,
                              notifier):
    """
    Create a graphviz file
    """
    lang = 'unknown'
    translations_manager.load_yaml_file(lang, lang_file)

    notifier.notify('Create "' + output_file + '"')
    translate = translations_manager.get_translateur(lang).translate

    yaml_file = open(output_file, 'wb')
    yaml_file.write(ci_manager.to_graphviz(translate).encode('utf-8'))
    yaml_file.close()

def execute():
    """ Execute the script, see module docstring for more details """
    parser = argparse.ArgumentParser(description='Create a graph of ci in a dot file(graphviz).')

    parser.add_argument('data_file',
                        help='the xml file of CI')

    parser.add_argument('lang_file',
                        help='The yml file used to translation')

    parser.add_argument('output_file',
                        help='The created file')

    parser.add_argument('-v', '--verbose', help='explain what is being done', action="store_true")

    args = parser.parse_args()

    notifier = Notifier(args.verbose)


    ci_manager = CentresOfInterestManager([], notifier)
    ci_manager.load_xml(args.data_file)

    translations_manager = TranslationsManager(notifier)

    create_graph_for_language(translations_manager,
                              ci_manager,
                              args.lang_file,
                              args.output_file,
                              notifier)

execute()
