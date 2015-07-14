"""
See Translateur class
"""

class Translateur:
    """
    A class used as a dict to translate simple sentences to a particular language.
    """

    @classmethod
    def untranslated_token(cls):
        """ return a token used to mark when no translation exist for a sentence """
        return "#untranslated#"

    def __init__(self, lang, iso_639_1, translations):
        """
        Contructor.

        :param lang: The language to where the sentences will be translated
        :param iso_639_1: https://en.wikipedia.org/wiki/ISO_639-1
        :param translations: a dict that associate sentences to translates sentences

        :type lang: str
        :type iso_639_1: str
        :type translations: dict
        """

        self.lang = lang
        self.iso_639_1 = iso_639_1
        self.translations = translations

    def translate(self, sentence):
        """ Translate a particular sentence """
        assert isinstance(sentence, str)
        if sentence in self.translations:
            if self.translations[sentence] == self.untranslated_token():
                return sentence + ' ' + self.untranslated_token()
            else:
                return self.translations[sentence]
        else:
            return None

    def add_translation(self, sentence, translation):
        """
        Add a particular translation.

        :param sentence: Original sentences
        :param translation: translated sentences

        :type sentence: str
        :type translation: str
        """

        assert isinstance(sentence, str)
        assert isinstance(translation, str)
        if sentence in self.translations:
            raise ValueError('sentence "' + sentence + '" is already translated')
        else:
            self.translations[sentence] = translation
