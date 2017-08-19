"""
Test TranslateurManager class
"""

import sys
import glob
import os
import shutil
import pytest
import yaml


sys.path.append('src')


from translations_manager import TranslationsManager
from translateur import Translateur
from centres_of_interest_manager import CentresOfInterestManager


def create_translations_tmp():
    if os.path.exists("./tests/translations_tmp"):
        shutil.rmtree("./tests/translations_tmp")
    shutil.copytree("./tests/translations", "./tests/translations_tmp")

def get_translations_manager():
    translations_manager = TranslationsManager()
    return translations_manager


def test_create_yaml_files():
    """ Test create_yaml_files method """
    if os.path.exists("./tests/translations_tmp"):
        shutil.rmtree("./tests/translations_tmp")
    os.mkdir("./tests/translations_tmp")
    translations_manager = TranslationsManager()
    translations_manager._create_yaml_file("./tests/translations_tmp/english.yml")
    dir_files = glob.glob('./tests/translations_tmp/*.yml')
    assert dir_files == ["./tests/translations_tmp/english.yml"]

def test_load_yaml_files():
    """ Test load_yaml_file method """
    translations_manager = get_translations_manager()
    create_translations_tmp()
    translations_manager.load_yaml_file("english", "./tests/translations_tmp/english.yml")

    translateur_en = translations_manager.get_translateur("english")
    assert translateur_en.translate("ci_1") == "ci oneéà€"
    assert translateur_en.translate("ci_2") == "ci two"
    assert translateur_en.translate("ci_3") == "ci three"
    assert translateur_en.translate("ci_4") == "ci four"
    assert translateur_en.translate("ci_5") == "ci five"

def test_save_yaml_file():
    """ Test save_in_yaml_files method """
    lang_file = "./tests/translations_tmp/english.yml"
    translations_manager = get_translations_manager()
    create_translations_tmp()
    translations_manager.load_yaml_file("english", lang_file)
    translateur = translations_manager.get_translateur('english')
    translateur.add_translation('ci_plop', 'ci_translated')
    translations_manager.save_yaml_file("english", lang_file)

    with open(lang_file, 'rb') as yml_file:
        translations = yaml.safe_load(yml_file)
        if translations is None:
            translations = {}

    assert 'ci_plop' in translations
    assert translations['ci_2'] == 'ci two'
    assert translations['ci_plop'] == 'ci_translated'

def test_fill_yaml_file():
    """ test fill_yaml_file """
    # TODO does not detect rewriting of already translated

    ci_manager = CentresOfInterestManager()
    ci_manager.load_xml("tests/ci_two_news.xml")
    translations_manager = get_translations_manager()
    create_translations_tmp()

    translations = {}
    untranslated_token = Translateur.untranslated_token()

    for lang in ['english', 'french']:
        lang_file = "./tests/translations_tmp/"+lang+".yml"
        translations_manager.fill_yaml_file(lang, lang_file, ci_manager)
        with open(lang_file, 'rb') as yml_file:
            translations[lang] = yaml.safe_load(yml_file)
            if translations[lang] is None:
                translations[lang] = {}
            translations[lang] = translations[lang]

    translations_wanted = {"ci_1":"ci oneéà€",
                           "ci_2":"ci two",
                           "ci_3":"ci three",
                           "ci_4":"ci four",
                           "ci_5":"ci five",
                           "ci_6":untranslated_token,
                           "ci_7":untranslated_token}

    assert translations["english"] == translations_wanted

    translations_wanted = {"ci_1":untranslated_token,
                           "ci_2":untranslated_token,
                           "ci_3":untranslated_token,
                           "ci_4":untranslated_token,
                           "ci_5":untranslated_token,
                           "ci_6":untranslated_token,
                           "ci_7":untranslated_token}

    assert translations["french"] == translations_wanted
