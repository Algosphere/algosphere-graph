#!/bin/python

import argparse
from CI_list import CI_list
from Translations_manager import Translations_manager
from mylib.Notifier import Notifier

parser = argparse.ArgumentParser(description='Fill yaml file of languages to begin translation')
parser.add_argument('input_file', help='the xml file of CI')
parser.add_argument('-l', '--lang', help='file with a list of the languages', default='languages.yml')
parser.add_argument('output_directory', help='the directory where to write yaml files')
parser.add_argument('-v', '--verbose', help='explain what is being done', action="store_true")

args = parser.parse_args()

notifier = Notifier(args.verbose)

ci_list = CI_list()

notifier.notify('load "' + args.input_file + '"')
ci_list.load_xml(args.input_file)


translations_manager = Translations_manager(args.lang, args.output_directory, notifier)

translations_manager.fill_yaml_file(ci_list)
