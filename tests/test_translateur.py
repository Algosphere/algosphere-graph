"""
Test Translateur class
"""

import unittest

from translateur import Translateur

class TranslaterTestCase(unittest.TestCase):
    """ A classic test class """

    def setUp(self):
        translations = {'ci 1':'ci one', 'ci 2':'ci two', 'ci 3':'ci three'}
        self.translateur = Translateur('english', 'en', translations)

    def test_translate(self):
        """ Test the translate method """
        translate = self.translateur.translate
        self.assertEqual(translate('ci 1'), 'ci one')
        self.assertEqual(translate('ci 2'), 'ci two')
        self.assertEqual(translate('ci 3'), 'ci three')
        self.assertEqual(translate('no ci'), None)

    def test_add_translation(self):
        """ Test the add_translation method """
        self.translateur.add_translation('ci 4', 'ci four')
        self.assertEqual(self.translateur.translate('ci 4'), 'ci four')

    def test_add_existing_translation(self):
        """ Test the add_translation method with a already existing translation """
        self.assertRaises(ValueError, self.translateur.add_translation, "ci 3", "ci three again")
