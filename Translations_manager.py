import yaml
import glob
import shutil
import os
import mylib.checking as checking
from mylib.Notifier import Notifier

from os.path import basename, splitext
from CI_list import CI_list
from Translateur import Translateur

class Translations_manager:
    def __init__(self, lang_file_name, output_directory, notifier = None):
        if(notifier != None):
            assert(isinstance(notifier, Notifier))

        self.notifier = notifier
        self.lang_file_name = lang_file_name
        self.output_directory = output_directory
        self.translateurs = {}
        with open(self.lang_file_name, 'r') as lang_file:
            self.notify('find languages in "' + self.lang_file_name + '"')
            self.languages = yaml.safe_load(lang_file)


    def notify(self, text):
        if(self.notifier != None):
            self.notifier.notify(text)

    def create_yaml_file(self):
        """for each languages, create a yaml file in directory if it does not already exist"""
        for lang in self.languages:
            file_name = self.output_directory + "/" + lang + ".yml"

            if not(os.path.exists(file_name)):
                self.notify('create "' + file_name + '"')
                new_file = open(file_name, "w")
                new_file.close()

    def load_yaml_file(self):
        self.translateurs = {}
        dir_files = glob.glob(self.output_directory + "/*.yml")
        for yml_file_name in dir_files:
            with open(yml_file_name, 'r') as yml_file:
                self.notify('open "' + yml_file_name + '"')
                lang = splitext(basename(yml_file_name))[0]
                iso_639_1 = self.languages[lang]
                translations = yaml.safe_load(yml_file)
                if(translations == None):
                    translations = {}
                self.translateurs[lang] = Translateur(lang, iso_639_1, translations)

    def save_in_yaml_file(self):
        shutil.rmtree(self.output_directory)
        os.mkdir(self.output_directory)
        for lang in self.languages:
            yml_file_name = self.output_directory + "/" + lang + ".yml"
            translations = self.translateurs[lang].translations
            with open(yml_file_name, 'w') as yml_file:
                self.notify('save "' + yml_file_name + '"')
                stream = yaml.dump(translations, default_flow_style=False, allow_unicode=True)
                yml_file.write(stream)

    def get_translateur(self, lang):
        return self.translateurs[lang]

    def fill_yaml_file(self, ci_list):
        """add the untranslated ci name of the ci_list at the end of each yaml file. (ci_name: untranslated)"""
        assert(isinstance(ci_list, CI_list))
        self.notify('create yaml files missing')
        self.create_yaml_file()
        self.notify('load all yaml files')
        self.load_yaml_file()

        self.notify('add missing items')
        ci_name_list = [ci.get_name() for ci in ci_list]

        for lang in self.get_languages():
            self.add_untranslated(ci_name_list, lang)

        self.notify('save all yaml files')
        self.save_in_yaml_file()

    def add_untranslated(self, ci_name_list, lang):
        assert(checking.is_all_instance(ci_name_list, str))
        assert(isinstance(lang, str))

        for ci_name in ci_name_list:
            if not(self.translateurs[lang].translate(ci_name)):
                self.notify('for language ' + lang + ' add a new item for "' + ci_name + '"')
                self.translateurs[lang].add_translation(ci_name, Translateur.untranslated_token())

    def get_languages(self):
        return self.languages
