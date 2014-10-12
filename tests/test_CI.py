import unittest
import sys
sys.path.append("..")

from CI import *

class CITestCase(unittest.TestCase):

    def setUp(self):
        self.ci = CI("some_name")

    def test_ci_creation(self):
        self.ci = CI("some_name")
        self.assertEqual(self.ci.get_name(), "some_name")

    def test_getter_and_setter(self):
        self.ci.set_name("new_name")
        self.assertEqual(self.ci.get_name(), "new_name")

        self.assertEqual(self.ci.get_url(), "")
        self.ci.set_url("url")
        self.assertEqual(self.ci.get_url(), "url")

        self.assertEqual(self.ci.get_date(), None)
        self.ci.set_date("date")
        self.assertEqual(self.ci.get_date(), "date")

        self.assertEqual(self.ci.get_children(), [])
        self.child_ci = CI("child_ci")
        self.ci.add_child(self.child_ci)
        self.assertEqual(self.ci.get_children(), [self.child_ci])

        self.assertEqual(self.ci.get_translations(), {})
        self.ci.add_translation("fr", "nouveau nom")
        self.assertEqual(self.ci.get_translations(), {"fr":"nouveau nom"})

    def test_translate(self):
        self.ci.add_translation("fr", "french name")
        self.assertEqual(self.ci.translate("en"), None)
        self.assertEqual(self.ci.translate("fr"), "french name")
