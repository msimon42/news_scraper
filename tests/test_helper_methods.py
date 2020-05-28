import pytest
from src.lib.helper_methods import *

class TestHelperMethods:
    def test_remove_null_values(self):
        test_list = ['hello', None, 'i', 'like', None, 'chikanz']
        new_list = remove_null_values(test_list)
        assert new_list == ['hello', 'i', 'like', 'chikanz']

    def test_n_days_ago(self):
        assert n_days_ago(2) == (datetime.now() - timedelta(days=2)).strftime('%m-%d-%y')
