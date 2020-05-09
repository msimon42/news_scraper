import re
import spacy
from spacy.tokenizer import Tokenizer

class NLProcessor:

    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
