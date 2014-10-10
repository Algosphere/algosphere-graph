#!/bin/python

# command line to transform ci.dot in ci.svg :
# dot -Tsvg ci.dot > ci.svg

import sys
from CI_list import CI_list

if(len(sys.argv) != 3):
    print("xml_to_graphviz.py ci.xml ci.dot")
    exit(1)

ci_list = CI_list([])
ci_list.load_xml(sys.argv[1])
a_file = open(sys.argv[2], 'w')


a_file.write(ci_list.to_graphviz())
a_file.close()
