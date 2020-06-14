from tests.config_tests import *

class TestSubscribe:
    def test_for_successful_response(self, client):
        response = client.get('/subscribe')
        assert response.status_code == 200
