import requests
from bs4 import BeautifulSoup
from .nl_processor import NLProcessor
from .helper_methods import *
from collections import Counter

class CssFinder:
    def __init__(self):
        self.nlp = NLProcessor()
        self.link_classes = Counter()

    def find_tag(self, url, user_agent=None):
        r = requests.get(url, headers=user_agent).content
        soup = BeautifulSoup(r, 'html.parser')
        links_with_sentence = [link for link in soup('a') if self.nlp.is_sentence(link.text, 'cssfind')]

        for link in links_with_sentence:
            self.__cssfind_hash_table(object=link)['link_class'][link.get('class') is None]

        return self.link_classes.most_common(1)[0][0]

    def __cssfind_hash_table(self, **kwargs):
        table = {
            'link_class': {
                True: self.__class_in_parent(kwargs['object']),
                False: self.__class_in_link(kwargs['object'])
            },
            'is_not_paragraph': {
                True: self.__update_counter(kwargs['object']),
                False: do_nothing()
            }
        }

        return table

    def __class_in_parent(self, link):
        try:
            css_class = link.parent.get('class')[0]
            self.__cssfind_hash_table(object=css_class)['is_not_paragraph'][self.nlp.phrase_length(link.parent.text) < 15]
        except:
            return None

    def __class_in_link(self, link):
        try:
            css_class = link.get('class')[0]
            self.__cssfind_hash_table(object=css_class)['is_not_paragraph'][self.nlp.phrase_length(link.text) < 15]
        except:
            return None


    def __update_counter(self, css_class):
        self.link_classes[css_class] += 1

from src.models import UserAgent
