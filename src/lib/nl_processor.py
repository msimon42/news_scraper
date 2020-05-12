import re
import spacy
from spacy.tokenizer import Tokenizer

class NLProcessor:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    def is_sentence(self, phrase):
        pos = set(self.find_parts_of_speech(phrase))
        deps = set(self.find_syntactic_relation(phrase))

        return len(pos.intersection(self.required_pos())) >= 2 and len(deps.intersection(self.required_deps())) >= 2


    def find_parts_of_speech(self, phrase):
        tokenized_phrase = self.nlp(phrase)
        token_pos = [ token.pos_ for token in tokenized_phrase ]
        return token_pos

    def find_syntactic_relation(self, phrase):
        tokenized_phrase = self.nlp(phrase)
        token_sr = [ token.dep_ for token in tokenized_phrase ]
        return token_sr

    def required_pos(self):
        return {'NOUN', 'VERB', 'DET'}

    def required_deps(self):
        return {'ROOT', 'nsubj', 'dobj'}