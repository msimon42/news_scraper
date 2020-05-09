import re
import spacy
from spacy.tokenizer import Tokenizer

class NLProcessor:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    @classmethod
    def is_sentence(cls, phrase):
        nlp = cls().nlp
        breakpoint()

    def find_parts_of_speech(self, phrase):
        tokenized_phrase = nlp(phrase)
        return token_pos = [ token.pos_ for token in tokenized_phrase ]





NLProcessor.is_sentence('The cat jumped over the moon.')
