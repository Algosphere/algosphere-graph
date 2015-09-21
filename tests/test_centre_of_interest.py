"""
Test CentreOfInterest class
"""

import pytest
import sys

sys.path.append('src')

from centre_of_interest import CentreOfInterest

def get_centre_of_interest():
    centre_of_interest = CentreOfInterest("some_name")
    return centre_of_interest

def test_ci_creation():
    """ Test creation of CentreOfInterest objects """
    centre_of_interest = get_centre_of_interest()
    assert centre_of_interest.name == "some_name"

def test_getter_and_setter():
    """ Test getter and setter """
    centre_of_interest = get_centre_of_interest()
    centre_of_interest.name = "new_name"
    assert centre_of_interest.name == "new_name"

    assert centre_of_interest.url == ""
    centre_of_interest.url = "url"
    assert centre_of_interest.url == "url"

    assert centre_of_interest.date == None
    centre_of_interest.date = "date"
    assert centre_of_interest.date == "date"

    assert centre_of_interest.children == []
    child_ci = CentreOfInterest("child_ci")
    centre_of_interest.add_child(child_ci)
    assert centre_of_interest.children == [child_ci]

    assert centre_of_interest.translations == {}
    centre_of_interest.add_translation("fr", "nouveau nom")
    assert centre_of_interest.translations == {"fr":"nouveau nom"}

def test_translate():
    """ Test translation of CI name """
    centre_of_interest = get_centre_of_interest()
    centre_of_interest.add_translation("fr", "french name")
    assert centre_of_interest.translate("en") == None
    assert centre_of_interest.translate("fr") == "french name"
