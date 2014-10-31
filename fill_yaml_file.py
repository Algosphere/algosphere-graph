#!/bin/python

import argparse
from CI_list import CI_list
from Translations_manager import Translations_manager

parser = argparse.ArgumentParser(description='Fill yaml file of languages to begin translation')
parser.add_argument('input_file', help='the xml file of CI')
parser.add_argument('-l', '--lang', help='file with a list of the languages', default='languages.yml')
parser.add_argument('output_directory', help='the directory where to write yaml files')

args = parser.parse_args()

ci_list = CI_list()
ci_list.load_xml(args.input_file)

translations_manager = Translations_manager(args.lang, args.output_directory)

translations_manager.fill_yaml_file(ci_list)
