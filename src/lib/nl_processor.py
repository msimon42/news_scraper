import re
import spacy
from spacy.tokenizer import Tokenizer

class NLProcessor:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    def is_sentence(self, phrase, *args, **kwargs):
        pos = set(self.find_parts_of_speech(phrase))
        deps = set(self.find_syntactic_relation(phrase))
        phrase_length = self.phrase_length(phrase)
        first_token = self.tokens_for(phrase)[0]

        results = [
            (len(pos.intersection(self.required_pos())) >= 2),
            (len(deps.intersection(self.required_deps())) >= 2),
            ((phrase_length > 6 and phrase_length < 12) or ('cssfind' not in args)),
            ((self.token_iscapitaized(first_token)) or ('cssfind' not in args))
        ]
        return all(results)


    def find_parts_of_speech(self, phrase):
        tokenized_phrase = self.tokens_for(phrase)
        token_pos = [ token.pos_ for token in tokenized_phrase ]
        return token_pos

    def find_syntactic_relation(self, phrase):
        tokenized_phrase = self.nlp(phrase)
        token_sr = [ token.dep_ for token in tokenized_phrase ]
        return token_sr

    def phrase_length(self, phrase):
        return len(self.nlp(phrase))

    def token_iscapitaized(self, token):
        return token.text[0].isupper()

    def tokens_for(self, phrase):
        return self.nlp(phrase)

    def required_pos(self):
        return {'NOUN', 'VERB', 'DET'}

    def required_deps(self):
        return {'ROOT', 'nsubj', 'dobj'}
