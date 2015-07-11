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
from mylib.Notifier import Notifier

def create_graph_for_language(translations_manager,
                              ci_manager,
                              lang,
                              output_directory,
                              base_name,
                              notifier):
    """
    Create a graphviz file for the language 'lang'
    """
    notifier.notify('create graph for language "' + lang +\
                    '" in directory "' + output_directory + '"')
    translate = translations_manager.get_translateur(lang).translate
    file_name = output_directory + base_name + '-' + lang + '.dot'
    yaml_file = open(file_name, 'wb')
    yaml_file.write(ci_manager.to_graphviz(translate).encode('utf-8'))
    yaml_file.close()

def execute():
    """ Execute the script, see module docstring for more details """
    parser = argparse.ArgumentParser(description='Create a graph of ci in a dot file(graphviz).')

    parser.add_argument('input_file', help='the xml file of CI')

    parser.add_argument('output_directory',
                        help='the directory where the dot file produced will go')

    parser.add_argument('-lf', '--lang_file', help='file with a list of the languages',
                        default='languages.yml')

    parser.add_argument('-d', '--yaml_directory',
                        help='the directory where to read yaml files for translations',
                        default='translations')

    parser.add_argument('-l', '--lang',
                        help='Languages in which the graphs are created, "all" for all languages',
                        default='all')

    parser.add_argument('-n', '--base_name',
                        help='The name in use to create the files, "base_name-lang.dot"',
                        default='ci')

    parser.add_argument('-v', '--verbose', help='explain what is being done', action="store_true")

    args = parser.parse_args()

    notifier = Notifier(args.verbose)

    ci_manager = CentresOfInterestManager([], notifier)
    ci_manager.load_xml(args.input_file)

    translations_manager = TranslationsManager(args.lang_file, args.yaml_directory, notifier)
    translations_manager.load_yaml_files()



    if args.lang != 'all':
        if args.lang in translations_manager.get_languages():
            create_graph_for_language(translations_manager,
                                      ci_manager,
                                      args.lang,
                                      args.output_directory,
                                      args.base_name, notifier)
        else:
            print(args.lang + ' unknown, look at the ' + args.yaml_directory + ' file')
    else:
        for lang in translations_manager.get_languages():
            create_graph_for_language(translations_manager,
                                      ci_manager,
                                      lang,
                                      args.output_directory,
                                      args.base_name, notifier)

execute()
