from src.lib.nl_processor import NLProcessor

class TestNLProcessor:
    def setup(self):
        self.nlp = NLProcessor()

    def test_is_sentence(self):
        phrase1 = 'Hello'
        phrase2 = 'Anti-Porn Filters Stop Dominic Cummings Trending On Twitter'
        phrase3 = 'Japan Enacts High-Tech Super City Bill Where AI, Big Data and Other Technologies Are Utilized To Resolve Social Problems'

        assert not self.nlp.is_sentence(phrase1)
        assert self.nlp.is_sentence(phrase2)
        assert not self.nlp.is_sentence(phrase3, 'cssfind')
        assert self.nlp.is_sentence(phrase3)

    def test_find_parts_of_speect(self):
        phrase = 'The cat jumped over the hill.'
        assert self.nlp.find_parts_of_speech(phrase) == ['DET', 'NOUN', 'VERB', 'ADP', 'DET', 'NOUN', 'PUNCT']

    def test_find_syntactic_relation(self):
        phrase = 'Proposed Bill Would Ban Microtargeting of Political Advertisements'
        assert self.nlp.find_syntactic_relation(phrase) == ['amod', 'nsubj', 'aux', 'ROOT', 'dobj', 'prep', 'amod', 'pobj']

    def test_preprocess_phrase(self):
        str1 = "\n   Hello frens"
        str2 = "This is a phrase\n"
        str3 = "\n\n\t   Denver Post uses tabs lol\t\t"

        assert self.nlp.preprocess_phrase(str1) == 'Hello frens'
        assert self.nlp.preprocess_phrase(str2) == 'This is a phrase'
        assert self.nlp.preprocess_phrase(str3) == 'Denver Post uses tabs lol'
