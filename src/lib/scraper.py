import requests
from bs4 import BeautifulSoup
from . import article
from . import link_processor

class Scraper:
    @classmethod
    def get_articles(cls, url, css_tag):
        r = requests.get(url).content
        soup = BeautifulSoup(r, 'html.parser')
        articles = soup.find_all(class_=css_tag)
        article_list = []
        for article in articles:
            if article.name != 'a':
                article = article.find('a')

            article_link = LinkProcessor.process(article.attrs['href'], url)
            article_list.append(Article(article.text, article_link))

        return article_list
