#!/bin/python

import argparse
from Translations_manager import Translations_manager

parser = argparse.ArgumentParser(description='Create a list of CI in a html file.')
parser.add_argument('input_file', help='file with a list of the lang')
parser.add_argument('output_directory', help='the directory where to write yaml files')

args = parser.parse_args()
translations_manager = Translations_manager(args.input_file)

translations_manager.create_yaml_file(args.output_directory)
