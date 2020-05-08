import requests
from bs4 import BeautifulSoup

class CssFinder:
    @classmethod
    def find_tag(cls, url):
        r = requests.get(url).content
        soup = BeautifulSoup(r, 'html.parser')
        link_elements = [link for link in soup('a') if NLProcessor.is_sentence(link.text)]

        for link in link_elements:
            class_ = link.get('class') if link.get('class') != None else




# CssFinder.find_tag('https://www.slashdot.org')
