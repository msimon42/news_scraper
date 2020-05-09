import re
import spacy
from spacy.tokenizer import Tokenizer

class NLProcessor:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    @classmethod
    def is_sentence(cls, phrase):
        nlp = cls().nlp
        tokenized_phrase = nlp(phrase)

        token_pos = [ token.pos_ for token in tokenized_phrase ]
        breakpoint()

        




NLProcessor.is_sentence('The cat jumped over the moon.')
