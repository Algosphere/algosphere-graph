#!/bin/python

"""
Fill the yaml translations file with the still untranslated centre of interest
for the choosen languages.

Usage: see '>>fill_yaml_file.py --help'
"""

import argparse
from centres_of_interest_manager import CentresOfInterestManager
from translations_manager import TranslationsManager
from mylib.Notifier import Notifier

def execute():
    """ Execute the script, see module docstring for more details """

    parser = argparse.ArgumentParser(description='Fill yaml file of languages to begin translation')
    parser.add_argument('input_file', help='the xml file of CI')
    parser.add_argument('-l', '--lang', help='file with a list of the languages',
                        default='languages.yml')
    parser.add_argument('output_directory', help='the directory where to write yaml files')
    parser.add_argument('-v', '--verbose', help='explain what is being done', action="store_true")

    args = parser.parse_args()

    notifier = Notifier(args.verbose)

    ci_manager = CentresOfInterestManager()

    notifier.notify('load "' + args.input_file + '"')
    ci_manager.load_xml(args.input_file)


    translations_manager = TranslationsManager(args.lang, args.output_directory, notifier)

    translations_manager.fill_yaml_file(ci_manager)

execute()
