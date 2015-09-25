#!/bin/python

"""
Create html files from a xml file describing a list of centres of interest.

Usage: see '>>xml_to_html_list.py --help'
"""


import sys
import argparse
sys.path.append('src')

from centres_of_interest_manager import CentresOfInterestManager
from translations_manager import TranslationsManager
from mylib.notifier import Notifier

def create_list_for_language(translations_manager,
                             ci_manager,
                             lang_file,
                             output_file,
                             notifier,
                             order):
    """
    Create a html file for the language 'lang'
    """
    lang = 'unknown'
    translations_manager.load_yaml_file(lang, lang_file)

    notifier.notify('Create "' + output_file + '"')
    translate = translations_manager.get_translateur(lang).translate
    html_file = open(output_file, 'wb')
    html_file.write(ci_manager.to_html_list(order, translate).encode('utf-8'))
    html_file.close()

def execute():
    """ Execute the script, see module docstring for more details """
    parser = argparse.ArgumentParser(description='Create a list of CI in a html file.')

    parser.add_argument('data_file', help='the xml file of CI')

    parser.add_argument('lang_file',
                        help='The yml file used to translation')

    parser.add_argument('output_file',
                        help='The created file')

    parser.add_argument('-sn', '--sort_by_name',
                        help='Sort the list by name',
                        action="store_true")

    parser.add_argument('-sd', '--sort_by_date',
                        help='Sort the list by date',
                        action="store_true")

    parser.add_argument('-v', '--verbose', help='explain what is being done', action="store_true")

    parser.add_argument('-oo', '--only_official', help='load only official CI', action="store_true")
    parser.add_argument('-l', '--with_link', help='add internet link to the list', action="store_true")

    args = parser.parse_args()

    notifier = Notifier(args.verbose)

    if args.sort_by_date and args.sort_by_name:
        notifier.notify("-sn is incompatible with -sd", 2)
        exit(1)

    if args.sort_by_date:
        notifier.notify('sorted by date')
        order = "by_date"
    else:
        notifier.notify('sorted by name')
        order = "by_name"

    ci_manager = CentresOfInterestManager([], notifier)
    ci_manager.load_xml(args.data_file, args.only_official, args.with_link)

    translations_manager = TranslationsManager(notifier)

    create_list_for_language(translations_manager,
                             ci_manager,
                             args.lang_file,
                             args.output_file,
                             notifier,
                             order)

execute()
