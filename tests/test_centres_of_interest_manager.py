"""
Test CentresOfInterestManager class
"""
#from proboscis import test # maybe we should use it for adding dependencies between test

import pytest
import sys

sys.path.append('src')

from centre_of_interest import CentreOfInterest
from centres_of_interest_manager import CentresOfInterestManager


def get_ci_manager():
    ci1 = CentreOfInterest("ci1")
    ci2 = CentreOfInterest("ci2")
    ci_manager = CentresOfInterestManager([ci1, ci2])
    return ci_manager

def test_append():
    """ Test the append method """
    ci_manager = get_ci_manager()
    ci1 = ci_manager._list_of_ci[0]
    ci2 = ci_manager._list_of_ci[1]
    ci3 = CentreOfInterest("ci3")
    ci_manager.append(ci3)
    assert ci_manager.list_of_ci == [ci1, ci2, ci3]

def test_iter():
    """ Test the __iter__ method """
    ci_manager = get_ci_manager()
    ci1 = ci_manager._list_of_ci[0]
    ci2 = ci_manager._list_of_ci[1]
    for (have, want) in zip(ci_manager, [ci1, ci2]):
        assert have == want

def test_find():
    """ Test the find method """
    ci_manager = get_ci_manager()
    ci1 = ci_manager._list_of_ci[0]
    ci2 = ci_manager._list_of_ci[1]
    assert ci_manager.find("ci2") == ci2
    assert ci_manager.find("unknow") == None

def test_load_xml():
    """ Test the load_xml method """
    ci_manager = get_ci_manager()
    ci_manager.load_xml("tests/ci.xml")
    assert len(ci_manager) == 5
    ci_1 = ci_manager.find("ci_1")
    ci_2 = ci_manager.find("ci_2")
    ci_3 = ci_manager.find("ci_3")
    ci_4 = ci_manager.find("ci_4")
    ci_5 = ci_manager.find("ci_5")
    list_of_ci = [ci_1, ci_2, ci_3, ci_4, ci_5]

    for (i, centre_of_interest) in zip(range(1, len(list_of_ci)+1), list_of_ci):
        assert centre_of_interest.url == "url"+str(i)

    assert ci_1.children == []
    assert ci_2.children == []
    assert ci_3.children == [ci_2]
    assert ci_4.children == [ci_1, ci_3]
    assert ci_5.children == [ci_1, ci_2]

def test_load_xml_with_bad_xml():
    """ Test the load_xml_with_bad_xml method """
    ci_manager = get_ci_manager()
    with pytest.raises(ValueError):
        ci_manager.load_xml("tests/bad_ci.xml")

def test_load_xml_with_bad_xml2():
    """ Test the load_xml_with_bad_xml method """
    ci_manager = get_ci_manager()
    with pytest.raises(ValueError):
        ci_manager.load_xml("tests/bad_ci2.xml")

def test_sorted_by_name():
    """ Test the sorted_by_name method """
    ci1 = CentreOfInterest("ci1")
    ci2 = CentreOfInterest("ci2")
    ci3 = CentreOfInterest("ci3")
    ci_manager = CentresOfInterestManager([ci2, ci1, ci3])
    assert ci_manager.sorted_by_name() == [ci1, ci2, ci3]

def test_sorted_by_date():
    """ Test the sorted_by_date method """
    ci1 = CentreOfInterest("ci1")
    ci2 = CentreOfInterest("ci2")
    ci3 = CentreOfInterest("ci3")
    ci1.date = "2014-01-02"
    ci2.date = "2014-01-02"
    ci3.date = "2014-01-01"
    ci_manager = CentresOfInterestManager([ci2, ci1, ci3])

    assert ci_manager.sorted_by_date() == [ci3, ci1, ci2]
