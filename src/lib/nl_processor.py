import re
import spacy
from spacy.tokenizer import Tokenizer

class NLProcessor:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    @classmethod
    def is_sentence(cls, phrase):
        nlp = cls()
        parts_of_speech = nlp.find_parts_of_speech(phrase)

        

    def find_parts_of_speech(self, phrase):
        tokenized_phrase = self.nlp(phrase)
        token_pos = [ token.pos_ for token in tokenized_phrase ]
        return token_pos

    def find_syntactic_relation(self, phrase):
        tokenized_phrase = self.nlp(phrase)
        token_sr = [ token.dep_ for token in tokenized_phrase ]
        return token_sr

    def required_pos(self):
        return ['NOUN', 'VERB', 'DET']

    def required_deps(self):
        return ['ROOT', 'nsubj', 'dobj']






# NLProcessor().find_syntactic_relation('15 free SVG illustration sets for your next project')
