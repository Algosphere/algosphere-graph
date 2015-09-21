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
        self.assertEqual(self.centre_of_interest.name, "some_name")

    def test_getter_and_setter(self):
        """ Test getter and setter """
        self.centre_of_interest.name = "new_name"
        self.assertEqual(self.centre_of_interest.name, "new_name")

        self.assertEqual(self.centre_of_interest.url, "")
        self.centre_of_interest.url = "url"
        self.assertEqual(self.centre_of_interest.url, "url")

        self.assertEqual(self.centre_of_interest.date, None)
        self.centre_of_interest.date = "date"
        self.assertEqual(self.centre_of_interest.date, "date")

        self.assertEqual(self.centre_of_interest.children, [])
        child_ci = CentreOfInterest("child_ci")
        self.centre_of_interest.add_child(child_ci)
        self.assertEqual(self.centre_of_interest.children, [child_ci])

        self.assertEqual(self.centre_of_interest.translations, {})
        self.centre_of_interest.add_translation("fr", "nouveau nom")
        self.assertEqual(self.centre_of_interest.translations, {"fr":"nouveau nom"})

    def test_translate(self):
        """ Test translation of CI name """
        self.centre_of_interest.add_translation("fr", "french name")
        self.assertEqual(self.centre_of_interest.translate("en"), None)
        self.assertEqual(self.centre_of_interest.translate("fr"), "french name")
