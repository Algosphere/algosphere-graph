"""
See Translations_manager class
"""

import yaml
import os
import copy
import mylib.checking as checking

from mylib.notifier import Notifier
from centres_of_interest_manager import CentresOfInterestManager
from translateur import Translateur

class TranslationsManager:
    """
    A class to manage tranlations of the centre of interests in different languages.
    """
    def __init__(self, notifier=None):
        if notifier != None:
            assert isinstance(notifier, Notifier)

        self._notifier = notifier
        self._translateurs = {}
        self._translateurs['up_to_date'] = {}

    def notify(self, text):
        """ Notify something happening to the user (use the Notifier object) """
        if self._notifier != None:
            self._notifier.notify(text)

    def _create_yaml_file(self, lang_file_name):
        """ For each languages, create a yaml file in directory if it does not already exist """

        if not os.path.exists(lang_file_name):
            self.notify('create "' + lang_file_name + '"')
            new_file = open(lang_file_name, "wb")
            new_file.close()

    def load_yaml_file(self, lang, lang_file_name):
        """ Load a yaml translation file. """

        with open(lang_file_name, 'rb') as yml_file:
            self.notify('open "' + lang_file_name + '"')
            translations = yaml.safe_load(yml_file)
            if translations == None:
                translations = {}
            self._translateurs[lang] = Translateur(lang, None, translations)
            self._translateurs['up_to_date'][lang] = True

    def save_yaml_file(self, lang, lang_file_name):
        """ Save the translations in the yaml file. """

        if self._translateurs['up_to_date'][lang] != True:
            translations = self._translateurs[lang].translations
            with open(lang_file_name, 'wb') as lang_file:
                self.notify('save "' + lang_file_name + '"')
                stream = yaml.dump(translations, default_flow_style=False, allow_unicode=True)
                lang_file.write(stream.encode('utf-8'))

    @property
    def languages(self):
        """ Get a dict of all languages """
        languages_name = copy.copy(self._translateurs)
        del languages_name['up_to_date']
        for key in languages_name:
            languages_name[key] = self._translateurs[key].iso_639_1
        return languages_name

    def get_translateur(self, lang):
        """ Get the translateur for the language 'lang'. """
        self._translateurs['up_to_date'][lang] = False
        return self._translateurs[lang]

    def fill_yaml_file(self, lang, lang_file_name, centres_of_interest_manager):
        """
        Add the untranslated ci name of the ci_list at the end of lang_file_name.
        syntax: 'ci_name: untranslated_token'
        """
        assert isinstance(centres_of_interest_manager, CentresOfInterestManager)

        ci_name_list = [ci.name for ci in centres_of_interest_manager]
        self._create_yaml_file(lang_file_name)
        self.load_yaml_file(lang, lang_file_name)
        self._add_untranslated(ci_name_list, lang)
        self.save_yaml_file(lang, lang_file_name)

    def _add_untranslated(self, ci_name_list, lang):
        """
        Add the untranslated ci name of the ci_name_list for the language 'lang',
        at the end of the corresponding yaml file.
        """
        assert checking.is_all_instance(ci_name_list, str)
        assert isinstance(lang, str)

        for ci_name in ci_name_list:
            if not self._translateurs[lang].translate(ci_name):
                self.notify('for language ' + lang + ' add a new item for "' + ci_name + '"')
                self._translateurs[lang].add_translation(ci_name, Translateur.untranslated_token())
                self._translateurs['up_to_date'][lang] = False

