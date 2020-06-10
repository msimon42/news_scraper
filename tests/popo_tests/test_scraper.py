from src.lib.scraper import Scraper

class TestScraper:
    def setup(self):
        self.scraper = Scraper()

    def test_ping(self):
        response1 = Scraper.ping('https://www.slashdot.org')
        response2 = Scraper.ping('https://www.bbc.com/news/jkhkjhkjh')
        assert response1 == 200
        assert response2 == 404

    def test_get_articles(self):
        response = self.scraper.get_articles('https://www.slashdot.org', 'story-title')
        assert str(type(response)) == "<class 'list'>"
        assert str(type(response[0])) == "<class 'src.lib.article_obj.ArticleObj'>"
