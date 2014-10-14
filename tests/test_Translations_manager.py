import unittest
import sys
import glob
import os
import shutil
sys.path.append("..")

from Translations_manager import Translations_manager
from CI_list import CI_list

class Translations_managerTestCase(unittest.TestCase):

    def setUp(self):
        self.translations_manager = Translations_manager("languages.yml", "translations")

    def test_constructor(self):
        self.assertEqual(self.translations_manager.get_languages(), {"french":"fr", "english":"en", "german":"de"})

    def test_create_yaml_file(self):
        shutil.rmtree("./translations2")
        os.mkdir("./translations2")
        self.translations_manager = Translations_manager("languages.yml", "translations2")

        self.translations_manager.create_yaml_file()
        dir_files = glob.glob('./translations2/*.yml')
        dir_files = sorted(dir_files)
        self.assertEqual(dir_files, ["./translations2/english.yml", "./translations2/french.yml", "./translations2/german.yml"])

    def test_load_yaml_file(self):
        self.translations_manager.load_yaml_file()

        translateur_en = self.translations_manager.get_translateur("english")
        self.assertEqual(translateur_en.translate("ci_1"), "ci one")
        self.assertEqual(translateur_en.translate("ci_2"), "ci two")
        self.assertEqual(translateur_en.translate("ci_3"), "ci three")
        self.assertEqual(translateur_en.translate("ci_4"), "ci four")
        self.assertEqual(translateur_en.translate("ci_5"), "ci five")

    def test_fill_yaml_file(self):
        ci_list = CI_list()
        ci_list.load_xml("ci.xml")
        # self.translations_manager.fill_yaml_file(ci_list)

