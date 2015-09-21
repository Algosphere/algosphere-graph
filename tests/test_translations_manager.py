"""
Test TranslateurManager class
"""

import unittest
import glob
import os
import shutil
import yaml


from translations_manager import TranslationsManager
from translateur import Translateur
from centres_of_interest_manager import CentresOfInterestManager

class TranslationsManagerTestCase(unittest.TestCase):
    """ A classic test class """

    def setUp(self):
        if os.path.exists("./tests/translations_tmp"):
            shutil.rmtree("./tests/translations_tmp")
        shutil.copytree("./tests/translations", "./tests/translations_tmp")
        self.translations_manager = TranslationsManager()

    def tearDown(self):
        pass
        # shutil.rmtree("./tests/translations_tmp")


    def test_create_yaml_files(self):
        """ Test create_yaml_files method """
        shutil.rmtree("./tests/translations_tmp")
        os.mkdir("./tests/translations_tmp")
        self.translations_manager = TranslationsManager()

        self.translations_manager._create_yaml_file("./tests/translations_tmp/english.yml")
        dir_files = glob.glob('./tests/translations_tmp/*.yml')
        self.assertEqual(dir_files, ["./tests/translations_tmp/english.yml"])

    def test_load_yaml_files(self):
        """ Test load_yaml_file method """
        self.translations_manager.load_yaml_file("english", "./tests/translations_tmp/english.yml")

        translateur_en = self.translations_manager.get_translateur("english")
        self.assertEqual(translateur_en.translate("ci_1"), "ci oneéà€")
        self.assertEqual(translateur_en.translate("ci_2"), "ci two")
        self.assertEqual(translateur_en.translate("ci_3"), "ci three")
        self.assertEqual(translateur_en.translate("ci_4"), "ci four")
        self.assertEqual(translateur_en.translate("ci_5"), "ci five")

    def test_save_yaml_file(self):
        """ Test save_in_yaml_files method """
        lang_file = "./tests/translations_tmp/english.yml"
        self.translations_manager.load_yaml_file("english", lang_file)
        translateur = self.translations_manager.get_translateur('english')
        translateur.add_translation('ci_plop', 'ci_translated')
        self.translations_manager.save_yaml_file("english", lang_file)

        with open(lang_file, 'rb') as yml_file:
            translations = yaml.safe_load(yml_file)
            if translations == None:
                translations = {}
        self.assertTrue('ci_plop' in translations)
        self.assertEqual(translations['ci_2'], 'ci two')
        self.assertEqual(translations['ci_plop'], 'ci_translated')

    def test_fill_yaml_file(self):
        """ test fill_yaml_file """
        # TODO does not detect rewriting of already translated

        ci_manager = CentresOfInterestManager()
        ci_manager.load_xml("tests/ci_two_news.xml")


        translations = {}
        untranslated_token = Translateur.untranslated_token()

        for lang in ['english', 'french']:
            lang_file = "./tests/translations_tmp/"+lang+".yml"
            self.translations_manager.fill_yaml_file(lang, lang_file, ci_manager)
            with open(lang_file, 'rb') as yml_file:
                translations[lang] = yaml.safe_load(yml_file)
                if translations[lang] == None:
                    translations[lang] = {}
                translations[lang] = translations[lang]

        translations_wanted = {"ci_1":"ci oneéà€",
                               "ci_2":"ci two",
                               "ci_3":"ci three",
                               "ci_4":"ci four",
                               "ci_5":"ci five",
                               "ci_6":untranslated_token,
                               "ci_7":untranslated_token}

        self.assertEqual(translations["english"], translations_wanted)

        translations_wanted = {"ci_1":untranslated_token,
                               "ci_2":untranslated_token,
                               "ci_3":untranslated_token,
                               "ci_4":untranslated_token,
                               "ci_5":untranslated_token,
                               "ci_6":untranslated_token,
                               "ci_7":untranslated_token}

        self.assertEqual(translations["french"], translations_wanted)
