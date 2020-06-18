from tests.config_tests import *

class TestConfirmationEmail:
    def test_confirmation_email(self):
        test_run = os.system('python manager.py test-confirmation')
        assert test_run == 0
