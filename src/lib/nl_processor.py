import re
import spacy
from spacy.tokenizer import Tokenizer

class NLProcessor:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    @classmethod
    def is_sentence(cls, phrase):
        nlp = cls()
        required_pos = ['VERB', 'NOUN', ]
        parts_of_speech = nlp.find_parts_of_speech(phrase)

        breakpoint()

    def find_parts_of_speech(self, phrase):
        tokenized_phrase = nlp(phrase)
        return token_pos = [ token.pos_ for token in tokenized_phrase ]

    def find_syntactic_relation(self, phrase):
        tokenized_phrase = nlp(phrase)
        return token_sr = [ token.dep_ for token in tokenized_phrase ]






NLProcessor.is_sentence('The cat jumped over the moon.')
