#!/bin/python

"""
Fill the yaml translations file with the still untranslated centre of interest
for the choosen languages.

Usage: see '>>fill_yaml_file.py --help'
"""

import argparse
from centres_of_interest_manager import CentresOfInterestManager
from translations_manager import TranslationsManager
from mylib.notifier import Notifier

def execute():
    """ Execute the script, see module docstring for more details """

    parser = argparse.ArgumentParser(description='Fill translation yaml file to begin translation')
    parser.add_argument('data_file', help='the xml file of CI')

    parser.add_argument('translation_file', help='The yaml file to update')

    parser.add_argument('-v', '--verbose', help='explain what is being done', action="store_true")

    args = parser.parse_args()

    notifier = Notifier(args.verbose)

    ci_manager = CentresOfInterestManager()

    notifier.notify('load "' + args.data_file + '"')
    ci_manager.load_xml(args.data_file)


    translations_manager = TranslationsManager(notifier)

    translations_manager.fill_yaml_file('unknows', args.translation_file, ci_manager)

execute()
