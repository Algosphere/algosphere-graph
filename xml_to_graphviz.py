#!/bin/python

import sys
from CI_list import CI_list

if(len(sys.argv) != 3):
    print("xml_to_graphviz.py ci.xml ci.dot")
    exit(1)

ci_list = CI_list([])
ci_list.load_xml(sys.argv[1])
a_file = open(sys.argv[2], 'w')

def to_graphviz(ci_list):
    assert(isinstance(ci_list, CI_list))
    string = "digraph CI {\n"
    for ci in ci_list:
        string += '    "' + ci.name + '";\n'

    string += "}"
    return replace_special_char(string)

def replace_special_char(string):
    return string
    special_char = ['é', 'è', 'ê', 'à', 'ù', 'û', 'ç', 'ô', 'î', 'ï', 'â']
    without_special_char = ['e', 'e', 'e', 'a', 'u', 'u', 'c', 'o', 'i', 'i', 'a']
    special_char += [x.upper() for x in special_char]
    without_special_char += [x.upper() for x in without_special_char]
    # special_char += ["<", "-", "'", ":", "’"]
    # without_special_char += ["a", "a", "a", "a", "a"]

    for (a, w_a) in zip(special_char, without_special_char):
        string = string.replace(a, w_a)

    return string


a_file.write(to_graphviz(ci_list))
a_file.close()
