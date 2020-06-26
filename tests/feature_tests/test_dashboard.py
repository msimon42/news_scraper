from test.config_tests import *

class TestDashboard:
    def test_for_successful_response(self, client):
        response = client.get(f'/dashboard?token={os.getenv('ADMIN_TOKEN')}')
        assert response.status_code == 200
