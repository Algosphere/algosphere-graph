#!/bin/python

# command line to transform ci.dot in ci.svg :
# dot -Tsvg ci.dot > ci.svg

import sys
from CI_list import CI_list

if(len(sys.argv) != 2):
    print("without_date.py ci.xml")
    exit(1)

ci_list = CI_list([])
ci_list.load_xml(sys.argv[1])

for ci in ci_list:
    if(ci.get_date() == None):
        print(ci.get_name())

