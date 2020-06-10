from src.lib.scraper import Scraper

class TestScraper:
    def setup(self):
        self.scraper = Scraper()

    def test_ping(self):
        response1 = Scraper.ping('https://www.slashdot.org')
        response2 = Scraper.ping('https://www.slashdot.org/fakenews')
        assert response1 == 200
        assert response2 == 404
