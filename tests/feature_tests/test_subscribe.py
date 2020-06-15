from tests.config_tests import *

class TestSubscribe:
    def test_for_successful_response(self, client):
        response = client.get('/subscribe')
        assert response.status_code == 200

    def test_for_subscribe_button(self, client):
        response = client.get('/subscribe')
        assert '<input class="button-line" id="submit-button" name="submit" type="submit" value="Subscribe">' in str(response.get_data()) 
