import requests
from bs4 import BeautifulSoup
from .nl_processor import NLProcessor
from collections import Counter

class CssFinder:
    def __init__(self):
        self.nlp = NLProcessor()
        self.link_classes = Counter()

    def find_tag(self, url):
        headers = random_user_agent_header()
        r = requests.get(url, headers=headers).content
        soup = BeautifulSoup(r, 'html.parser')
        links_with_sentence = [link for link in soup('a') if self.nlp.is_sentence(link.text, 'cssfind')]
        link_classes = Counter()

        for link in links_with_sentence:
            if link.get('class') is None:
                try:
                    css_class = link.parent.get('class')[0]
                except:
                    continue

                link_classes[css_class] += 1 if self.nlp.phrase_length(link.parent.text) < 10
                continue

            css_class = link.get('class')[0]
            link_classes[css_class] += 1

        return link_classes.most_common(1)[0][0]

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
            return link.parent.get('class')[0]
        except:
            return None


from .helper_methods import *
