import requests
from bs4 import BeautifulSoup
from .nl_processor import NLProcessor
from collections import Counter

class CssFinder:
    @classmethod
    def find_tag(cls, url):
        r = requests.get(url).content
        soup = BeautifulSoup(r, 'html.parser')
        nlp = NLProcessor()
        links_with_sentence = [link for link in soup('a') if nlp.is_sentence(link.text, 'cssfind')]
        link_classes = Counter()

        for link in links_with_sentence:
            if link.get('class') is None:
                try:
                    css_class = link.parent.get('class')[0]
                except:
                    continue

                link_classes[css_class] += 1
                continue

            css_class = link.get('class')[0]
            link_classes[css_class] += 1
        return link_classes.most_common(1)[0][0]
