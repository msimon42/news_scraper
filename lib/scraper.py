import requests
from bs4 import BeautifulSoup

class Scraper:
    @classmethod
    def get_slashdot_articles(cls):
        url = 'http://www.slashdot.org'
        r = requests.get(url).content
        soup = BeautifulSoup(r, 'html.parser')
        articles = soup.find_all('article')
        for link in articles:
            print(link)

Scraper.get_slashdot_articles()
