#!/bin/python

"""
Get all the centres of interest without date.

Usage: without_date.py ci.xml

command line to transform ci.dot in ci.svg :
dot -Tsvg ci.dot > ci.svg
"""


import sys
sys.path.append('src')

from centres_of_interest_manager import CentresOfInterestManager

if len(sys.argv) != 2:
    print("without_date.py ci.xml")
    exit(1)

def execute():
    """ Execute the script, see module docstring for more details """
    ci_manager = CentresOfInterestManager([])
    ci_manager.load_xml(sys.argv[1])

    for centre_of_interest in ci_manager:
        if centre_of_interest.date == None:
            print(centre_of_interest.name)

execute()

