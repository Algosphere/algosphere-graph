"""
Test CentreOfInterest class
"""

import unittest

from centre_of_interest import CentreOfInterest

class CentreOfInterestTestCase(unittest.TestCase):
    """ A classic test class """

    def setUp(self):
        self.centre_of_interest = CentreOfInterest("some_name")

    def test_ci_creation(self):
        """ Test creation of CentreOfInterest objects """
        self.centre_of_interest = CentreOfInterest("some_name")
        self.assertEqual(self.centre_of_interest.get_name(), "some_name")

    def test_getter_and_setter(self):
        """ Test getter and setter """
        self.centre_of_interest.set_name("new_name")
        self.assertEqual(self.centre_of_interest.get_name(), "new_name")

        self.assertEqual(self.centre_of_interest.get_url(), "")
        self.centre_of_interest.set_url("url")
        self.assertEqual(self.centre_of_interest.get_url(), "url")

        self.assertEqual(self.centre_of_interest.get_date(), None)
        self.centre_of_interest.set_date("date")
        self.assertEqual(self.centre_of_interest.get_date(), "date")

        self.assertEqual(self.centre_of_interest.get_children(), [])
        child_ci = CentreOfInterest("child_ci")
        self.centre_of_interest.add_child(child_ci)
        self.assertEqual(self.centre_of_interest.get_children(), [child_ci])

        self.assertEqual(self.centre_of_interest.get_translations(), {})
        self.centre_of_interest.add_translation("fr", "nouveau nom")
        self.assertEqual(self.centre_of_interest.get_translations(), {"fr":"nouveau nom"})

    def test_translate(self):
        """ Test translation of CI name """
        self.centre_of_interest.add_translation("fr", "french name")
        self.assertEqual(self.centre_of_interest.translate("en"), None)
        self.assertEqual(self.centre_of_interest.translate("fr"), "french name")
