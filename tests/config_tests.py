from application import create_application
import os
import pytest

@pytest.fixture
def client():
    app = create_application()
    app.config['SECRET_KEY'] = os.urandom(32)
    test_app = app.test_client()
    return test_app
