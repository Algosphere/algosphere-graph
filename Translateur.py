
class Translateur:
    def __init__(self, name, iso_639_1, translations):
        self.name = name
        self.iso_639_1 = iso_639_1
        self.translations = translations

    def translate(self, sentence):
        assert(isinstance(sentence, str))
        return self.translations[sentence]

