from application import create_application
import pytest

@pytest.fixture
def client():
    app = create_application()
    test_app = app.test_client()
    return test_app
