#!/bin/python

# command line to transform ci.dot in ci.svg :
# dot -Tsvg ci.dot > ci.svg

import sys
import argparse
from CI_list import CI_list

parser = argparse.ArgumentParser(description='Create a graph of ci in a dot file(graphviz).')
parser.add_argument('input_file', help='the xml file of CI')
parser.add_argument('output_file', help='the name of the dot file produced')

args = parser.parse_args()

ci_list = CI_list([])
ci_list.load_xml(args.input_file)
a_file = open(args.output_file, 'w')


a_file.write(ci_list.to_graphviz())
a_file.close()
