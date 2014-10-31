
class Translateur:
    def __init__(self, lang, iso_639_1, translations):
        self.lang = lang
        self.iso_639_1 = iso_639_1
        self.translations = translations

    def translate(self, sentence):
        assert(isinstance(sentence, str))
        if(sentence in self.translations):
            return self.translations[sentence]
        else:
            return None

    def add_translation(self, sentence, translation):
        assert(isinstance(sentence, str))
        assert(isinstance(translation, str))
        if(sentence in self.translations):
            raise ValueError('sentence "' + sentence + '" is already translated')
        else:
            self.translations[sentence] = translation
