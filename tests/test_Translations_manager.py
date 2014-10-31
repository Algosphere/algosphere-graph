import unittest
import sys
import glob
import os
import shutil
import yaml
sys.path.append("..")

from Translations_manager import Translations_manager
from CI_list import CI_list

class Translations_managerTestCase(unittest.TestCase):

    def setUp(self):
        shutil.copytree("./translations", "./translations_tmp")
        self.translations_manager = Translations_manager("languages.yml", "translations_tmp/")

    def tearDown(self):
        shutil.rmtree("./translations_tmp")

    def test_constructor(self):
        self.assertEqual(self.translations_manager.get_languages(), {"french":"fr", "english":"en", "german":"de"})

    def test_create_yaml_file(self):
        shutil.rmtree("./translations_tmp")
        os.mkdir("./translations_tmp")
        self.translations_manager = Translations_manager("languages.yml", "translations_tmp")

        self.translations_manager.create_yaml_file()
        dir_files = glob.glob('./translations_tmp/*.yml')
        dir_files = sorted(dir_files)
        self.assertEqual(dir_files, ["./translations_tmp/english.yml", "./translations_tmp/french.yml", "./translations_tmp/german.yml"])

    def test_load_yaml_file(self):
        self.translations_manager.load_yaml_file()

        translateur_en = self.translations_manager.get_translateur("english")
        self.assertEqual(translateur_en.translate("ci_1"), "ci oneéà€")
        self.assertEqual(translateur_en.translate("ci_2"), "ci two")
        self.assertEqual(translateur_en.translate("ci_3"), "ci three")
        self.assertEqual(translateur_en.translate("ci_4"), "ci four")
        self.assertEqual(translateur_en.translate("ci_5"), "ci five")

    def test_save_in_yaml_file(self):
        self.translations_manager.load_yaml_file()
        translateur = self.translations_manager.get_translateur('english')
        translateur.add_translation('ci_plop', 'ci_translated')
        self.translations_manager.save_in_yaml_file()
        with open("./translations_tmp/english.yml", 'r') as yml_file:
            translations = yaml.safe_load(yml_file)
            if(translations == None):
                translations = {}
        if('ci_plop' in translations):
            self.assertEqual(translations['ci_2'], 'ci two')
            self.assertEqual(translations['ci_plop'], 'ci_translated')
        else:
            self.assertTrue(False)

    def test_fill_yaml_file(self):
        # TODO does not detect rewriting of already translated
        ci_list = CI_list()
        ci_list.load_xml("ci_two_news.xml")
        self.translations_manager.fill_yaml_file(ci_list)
        translations = {}
        untranslated_token = self.translations_manager.untranslated_token
        for lang in self.translations_manager.get_languages():
            with open("./translations_tmp/"+lang+".yml", 'r') as yml_file:
                translations[lang] = yaml.safe_load(yml_file)
                if(translations[lang] == None):
                    translations[lang] = {}
                translations[lang] = translations[lang]

        translations_wanted = {"ci_1":"ci oneéà€", "ci_2":"ci two", "ci_3":"ci three", "ci_4":"ci four", "ci_5":"ci five", "ci_6":untranslated_token, "ci_7":untranslated_token}
        self.assertEqual(translations["english"], translations_wanted)

        translations_wanted = {"ci_1":untranslated_token, "ci_2":untranslated_token, "ci_3":untranslated_token, "ci_4":untranslated_token, "ci_5":untranslated_token, "ci_6":untranslated_token, "ci_7":untranslated_token}
        self.assertEqual(translations["french"], translations_wanted)
