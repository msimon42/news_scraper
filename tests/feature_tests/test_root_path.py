from tests.config_tests import *

class TestRootPath:
    def test_root(self, client):
        response = client.get('/')
        assert response.status_code == 200
