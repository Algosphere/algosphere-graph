#!/bin/python

# command line to transform ci.dot in ci.svg :
# dot -Tsvg ci.dot > ci.svg

import sys
import argparse
from CI_list import CI_list
from Translations_manager import Translations_manager
from mylib.Notifier import Notifier

def create_list_for_language(translations_manager, lang, output_directory, base_name, notifier, order):
    notifier.notify('create list for language "' + lang + '" in directory "' + output_directory + '"')
    translate = translations_manager.get_translateur(lang).translate
    file_name = output_directory + base_name + '-' + lang + '.html'
    html_file = open(file_name, 'w')
    html_file.write(ci_list.to_html_list(order, translate))
    html_file.close()

parser = argparse.ArgumentParser(description='Create a list of CI in a html file.')
parser.add_argument('input_file', help='the xml file of CI')
parser.add_argument('output_directory', help='the directory where the html file produced will go')
parser.add_argument('-lf', '--lang_file', help='file with a list of the languages', default='languages.yml')
parser.add_argument('-d', '--yaml_directory', help='the directory where to read yaml files for translations', default='translations')
parser.add_argument('-l', '--lang', help='Languages in which the lists are created, "all" for all languages', default='all')
parser.add_argument('-n', '--base_name', help='The name in use to create the files, "base_name-lang.html"', default='ci')
parser.add_argument('-sn','--sort_by_name', help='Sort the list by name', action="store_true")
parser.add_argument('-sd', '--sort_by_date', help='Sort the list by date', action="store_true")
parser.add_argument('-v', '--verbose', help='explain what is being done', action="store_true")

args = parser.parse_args()

notifier = Notifier(args.verbose)

if(args.sort_by_date and args.sort_by_name):
    notifier.notify("-sn is incompatible with -sd", 2)
    exit(1)

if(args.sort_by_date):
    notifier.notify('sorted by date')
    order = "by_date"
else:
    notifier.notify('sorted by name')
    order = "by_name"

ci_list = CI_list([], notifier)
ci_list.load_xml(args.input_file)

translations_manager = Translations_manager(args.lang_file, args.yaml_directory, notifier)
translations_manager.load_yaml_file()

if(args.lang != 'all'):
    if(args.lang in translations_manager.get_languages()):
        create_list_for_language(translations_manager, args.lang, args.output_directory, args.base_name, notifier, order)
    else:
        print(args.lang + ' unknown, look at the ' + args.yaml_directory + ' file')
else:
    for lang in translations_manager.get_languages():
        create_list_for_language(translations_manager, lang, args.output_directory, args.base_name, notifier, order)

