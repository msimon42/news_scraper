import requests
from bs4 import BeautifulSoup
from article import Article

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

            article_list.append(Article(article.text, f"{article.attrs['href']}"))

        return article_list
