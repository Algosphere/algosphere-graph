import yaml
import glob

from os.path import basename, splitext
from CI_list import CI_list
from Translateur import Translateur

class Translations_manager:
    def __init__(self, lang_file_name, output_directory):
        self.lang_file_name = lang_file_name
        self.output_directory = output_directory
        self.translateurs = {}
        with open(self.lang_file_name, 'r') as lang_file:
            self.languages = yaml.load(lang_file)

    def create_yaml_file(self):
        """for each languages, create a yaml file in directory if it does not already exist"""
        dir_files = glob.glob(self.output_directory + "/*.yml")
        for lang in self.languages:
            file_name = self.output_directory + "/" + lang + ".yml"
            if not(file_name in dir_files):
                new_file = open(file_name, "w")
                new_file.close()

    def load_yaml_file(self):
        dir_files = glob.glob(self.output_directory + "/*.yml")
        for yml_file_name in dir_files:
            with open(yml_file_name, 'r') as yml_file:
                lang = splitext(basename(yml_file_name))[0]
                iso_639_1 = self.languages[lang]
                translations = yaml.load(yml_file)
                self.translateurs[lang] = Translateur(lang, iso_639_1, translations)

    def get_translateur(self, lang):
        return self.translateurs[lang]

    def fill_yaml_file(self, ci_list):
        """add the untranslated ci name of the ci_list at the end of each yaml file. (ci_name: untranslated)"""
        assert(isinstance(ci_list, CI_list))
        dir_files = glob.glob(self.output_directory + "/*.yml")
        ci_name_list = [ci.get_name() for ci in ci_list]
        ci_name_dict = dict(zip(ci_name_list, ci_name_list))

        for yml_file_name in dir_files:
            with open(yml_file_name, 'w') as yml_file:
                yaml.dump(ci_name_dict, yml_file, default_flow_style=False)

    def get_languages(self):
        return self.languages
