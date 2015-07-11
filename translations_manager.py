"""
See Translations_manager class
"""

import yaml
import glob
import shutil
import os
import mylib.checking as checking

from mylib.Notifier import Notifier
from os.path import basename, splitext
from centres_of_interest_manager import CentresOfInterestManager
from translateur import Translateur

class TranslationsManager:
    """
    A class to manage tranlations of the centre of interests in different languages.
    """
    def __init__(self, lang_file_name, translations_directory, notifier=None):
        if notifier != None:
            assert isinstance(notifier, Notifier)

        self.notifier = notifier
        self.lang_file_name = lang_file_name
        self.translations_directory = translations_directory
        self.translateurs = {}
        with open(self.lang_file_name, 'rb') as lang_file:
            self.notify('find languages in "' + self.lang_file_name + '"')
            self.languages = yaml.safe_load(lang_file)


    def notify(self, text):
        """ Notify something happening to the user (use the Notifier object) """
        if self.notifier != None:
            self.notifier.notify(text)

    def create_yaml_files(self):
        """ For each languages, create a yaml file in directory if it does not already exist """
        for lang in self.languages:
            file_name = self.translations_directory + "/" + lang + ".yml"

            if not os.path.exists(file_name):
                self.notify('create "' + file_name + '"')
                new_file = open(file_name, "wb")
                new_file.close()

    def load_yaml_files(self):
        """ Load the yaml translations files in the translations_directory. """
        self.translateurs = {}
        dir_files = glob.glob(self.translations_directory + "/*.yml")
        for yml_file_name in dir_files:
            with open(yml_file_name, 'rb') as yml_file:
                self.notify('open "' + yml_file_name + '"')
                lang = splitext(basename(yml_file_name))[0]
                iso_639_1 = self.languages[lang]
                translations = yaml.safe_load(yml_file)
                if translations == None:
                    translations = {}
                self.translateurs[lang] = Translateur(lang, iso_639_1, translations)

    def save_in_yaml_files(self):
        """ Save the translations in the yaml translations files. """
        shutil.rmtree(self.translations_directory)
        os.mkdir(self.translations_directory)
        for lang in self.languages:
            yml_file_name = self.translations_directory + lang + ".yml"
            translations = self.translateurs[lang].translations
            with open(yml_file_name, 'wb') as yml_file:
                self.notify('save "' + yml_file_name + '"')
                stream = yaml.dump(translations, default_flow_style=False, allow_unicode=True)
                yml_file.write(stream.encode('utf-8'))

    def get_translateur(self, lang):
        """ Get the translateur for the language 'lang'. """
        return self.translateurs[lang]

    def fill_yaml_file(self, centres_of_interest_manager):
        """
        Add the untranslated ci name of the ci_list at the end of each yaml file.
        syntax: 'ci_name: untranslated'
        """
        assert isinstance(centres_of_interest_manager, CentresOfInterestManager)
        self.notify('create yaml files missing')
        self.create_yaml_files()
        self.notify('load all yaml files')
        self.load_yaml_files()

        self.notify('add missing items')
        ci_name_list = [ci.get_name() for ci in centres_of_interest_manager]

        for lang in self.get_languages():
            self._add_untranslated(ci_name_list, lang)

        self.notify('save all yaml files')
        self.save_in_yaml_files()

    def _add_untranslated(self, ci_name_list, lang):
        """
        Add the untranslated ci name of the ci_name_list for the language 'lang',
        at the end of the corresponding yaml file.
        """
        assert checking.is_all_instance(ci_name_list, str)
        assert isinstance(lang, str)

        for ci_name in ci_name_list:
            if not self.translateurs[lang].translate(ci_name):
                self.notify('for language ' + lang + ' add a new item for "' + ci_name + '"')
                self.translateurs[lang].add_translation(ci_name, Translateur.untranslated_token())

    def get_languages(self):
        """ Get all the managed languages, see lang_file_name """
        return self.languages
