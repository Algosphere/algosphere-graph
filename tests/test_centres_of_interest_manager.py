"""
Test CentresOfInterestManager class
"""

import unittest
#from proboscis import test # maybe we should use it for adding dependencies between test

# sys.path.append("..")

from centre_of_interest import CentreOfInterest
from centres_of_interest_manager import CentresOfInterestManager

class CentresOfInterestManagerTestCase(unittest.TestCase):
    """ A classic test class """

    def setUp(self):
        self.ci1 = CentreOfInterest("ci1")
        self.ci2 = CentreOfInterest("ci2")
        self.ci3 = CentreOfInterest("ci3")
        self.ci_manager = CentresOfInterestManager([self.ci1, self.ci2])

    def test_append(self):
        """ Test the append method """
        self.ci_manager.append(self.ci3)
        self.assertEqual(self.ci_manager.get_list_of_ci(), [self.ci1, self.ci2, self.ci3])

    def test_iter(self):
        """ Test the __iter__ method """
        for (have, want) in zip(self.ci_manager, [self.ci1, self.ci2]):
            with self.subTest(i=(have, want)):
                self.assertEqual(have, want)

    def test_find(self):
        """ Test the find method """
        self.assertEqual(self.ci_manager.find("ci2"), self.ci2)
        self.assertEqual(self.ci_manager.find("unknow"), None)

    def test_load_xml(self):
        """ Test the load_xml method """
        self.ci_manager.load_xml("tests/ci.xml")
        self.assertEqual(len(self.ci_manager), 5)
        ci_1 = self.ci_manager.find("ci_1")
        ci_2 = self.ci_manager.find("ci_2")
        ci_3 = self.ci_manager.find("ci_3")
        ci_4 = self.ci_manager.find("ci_4")
        ci_5 = self.ci_manager.find("ci_5")
        list_of_ci = [ci_1, ci_2, ci_3, ci_4, ci_5]

        for (i, centre_of_interest) in zip(range(1, len(list_of_ci)+1), list_of_ci):
            with self.subTest(i=i):
                self.assertEqual(centre_of_interest.get_url(), "url"+str(i))

        self.assertEqual(ci_1.get_children(), [])
        self.assertEqual(ci_2.get_children(), [])
        self.assertEqual(ci_3.get_children(), [ci_2])
        self.assertEqual(ci_4.get_children(), [ci_1, ci_3])
        self.assertEqual(ci_5.get_children(), [ci_1, ci_2])

    def test_load_xml_with_bad_xml(self):
        """ Test the load_xml_with_bad_xml method """
        self.assertRaises(ValueError, self.ci_manager.load_xml, "tests/bad_ci.xml")

    def test_load_xml_with_bad_xml2(self):
        """ Test the load_xml_with_bad_xml method """
        self.assertRaises(ValueError, self.ci_manager.load_xml, "tests/bad_ci2.xml")

    def test_sorted_by_name(self):
        """ Test the sorted_by_name method """
        self.ci_manager = CentresOfInterestManager([self.ci2, self.ci1, self.ci3])
        self.assertEqual(self.ci_manager.sorted_by_name(), [self.ci1, self.ci2, self.ci3])

    def test_sorted_by_date(self):
        """ Test the sorted_by_date method """
        self.ci1.set_date("2014-01-02")
        self.ci2.set_date("2014-01-02")
        self.ci3.set_date("2014-01-01")
        self.ci_manager = CentresOfInterestManager([self.ci2, self.ci1, self.ci3])

        self.assertEqual(self.ci_manager.sorted_by_date(), [self.ci3, self.ci1, self.ci2])
