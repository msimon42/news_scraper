import requests
from bs4 import BeautifulSoup

class Scraper:
    @classmethod
    def get_slashdot_articles():
        uri = 'http://www.slashdot.org/popular'
        
