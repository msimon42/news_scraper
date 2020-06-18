from tests.config_tests import *

class TestNewsletter:
    def test_newsletter(self):
        test_run = os.system('python manager.py test-newsletter')
        assert test_run == 0
