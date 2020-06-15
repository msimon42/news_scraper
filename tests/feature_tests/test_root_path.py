from tests.config_tests import *

class TestRootPath:
    def test_for_successful_response(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_for_news_scraper(self, client):
        response = client.get('/')
        assert 'News Scraper' in str(response.get_data())

    def test_for_subscribe_button(self, client):
        response = client.get('/')
        assert '<a class="button-line" href="/subscribe">Subscribe</a>' in str(response.get_data())
