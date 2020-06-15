from tests.config_tests import *

class TestSubscribe:
    def test_for_successful_response(self, client):
        response = client.get('/subscribe')
        assert response.status_code == 200

    def test_for_subscribe_button(self, client):
        response = client.get('/subscribe')
        assert '<input class="button-line" id="submit-button" name="submit" type="submit" value="Subscribe">' in str(response.get_data())

    def test_for_email_field(self, client):
        response = client.get('/subscribe')
        assert '<input id="email" name="email" placeholder="email@example.com" type="text" value="">' in str(response.get_data())

    def test_links_field(self, client):
        response = client.get('/subscribe')
        assert '<input id="links" name="links" placeholder="https://www.example.com/news,http://www.news.org, etc." type="text" value="">' in str(response.get_data())     
