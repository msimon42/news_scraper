import requests
from bs4 import BeautifulSoup

class Scraper:
    @classmethod
    def get_slashdot_articles(cls):
        url = 'http://www.slashdot.org'
        r = requests.get(url).content
        soup = BeautifulSoup(r, 'html.parser')
        articles = soup.find_all(class_='story-title')
        article_list = []
        for article in articles:
            link = article.find('a')
            article_list.append(Article(link.text, link.attrs['href']))

        return article_list    

Scraper.get_slashdot_articles()
