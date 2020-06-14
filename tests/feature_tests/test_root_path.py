from tests.config_tests import *

class TestRootPath:
    def test_root(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_for_news_scraper(self, client):
        response = client.get('/')
        assert 'News Scraper' in str(response.get_data())    
