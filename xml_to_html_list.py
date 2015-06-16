#!/bin/python

# command line to transform ci.dot in ci.svg :
# dot -Tsvg ci.dot > ci.svg

import sys
import argparse
from CI_list import CI_list
from mylib.Notifier import Notifier

parser = argparse.ArgumentParser(description='Create a list of CI in a html file.')
parser.add_argument('-n','--by_name', help='Sort the list by name', action="store_true")
parser.add_argument('-d', '--by_date', help='Sort the list by date', action="store_true")
parser.add_argument('input_file', help='the xml file of CI')
parser.add_argument('output_file', help='the name of the html file produced')
parser.add_argument('-v', '--verbose', help='explain what is being done', action="store_true")

args = parser.parse_args()

notifier = Notifier(args.verbose)

if(args.by_date and args.by_name):
    notifier.notify("-n is incompatible with -d", 2)
    exit(1)

if(args.by_date):
    notifier.notify('order by date')
    order = "by_date"
else:
    notifier.notify('order by name')
    order = "by_name"

ci_list = CI_list([])
ci_list.load_xml(args.input_file, notifier)

notifier.notify('create html file "' + args.output_file + '"')

a_file = open(args.output_file, 'w')
a_file.write(ci_list.to_html_list(order))
a_file.close()
