import requests
from bs4 import BeautifulSoup

class Scraper:
    @classmethod
    def get_slashdot_articles(cls):
        uri = 'http://www.slashdot.org/popular'
        r = requests.get(uri).content
        soup = BeautifulSoup(r, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            print(f"{link.text}, {link.attrs}")

Scraper.get_slashdot_articles()
