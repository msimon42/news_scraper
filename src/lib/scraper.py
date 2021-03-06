import requests
from bs4 import BeautifulSoup
from .article_obj import ArticleObj
from .link_processor import LinkProcessor
from .nl_processor import NLProcessor
from .helper_methods import *

class Scraper:
    def __init__(self):
        self.nlp = NLProcessor()

    def get_articles(self, url, css_tag, **kwargs):
        headers = kwargs['user_agent']
        r = requests.get(url, headers=headers).content
        soup = BeautifulSoup(r, 'html.parser')
        articles = soup.find_all(class_=css_tag)
        article_list = []
        for article in articles:
            if article.name != 'a':
                article_link_elements = article.find_all('a')
                for link in article_link_elements:
                    article_list.append(self.__filter_and_convert_link_element(link, url, save=kwargs['save'], link_id=kwargs['link_id']))

            elif article.name == 'a':
                article_list.append(self.__filter_and_convert_link_element(article, url, save=kwargs['save'], link_id=kwargs['link_id']))

        return remove_null_values(article_list)

    def __filter_and_convert_link_element(self, link_element, url, **kwargs):
        article_link = LinkProcessor.process(link_element.get('href'), url)
        if self.nlp.is_sentence(link_element.text):
            a = ArticleObj(self.nlp.preprocess_phrase(link_element.text), article_link)
            if kwargs['save'] is True:
                a.save_to_db(kwargs['link_id'])

            return a

    @classmethod
    def ping(cls, url):
        r = requests.get(url)
        return r.status_code
