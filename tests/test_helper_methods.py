import pytest
from src.lib.helper_methods import *

class TestHelperMethods:
    def test_remove_null_values(self):
        test_list = ['hello', None, 'i', 'like', None, 'chikanz']
        new_list = remove_null_values(test_list)
        assert new_list == ['hello', 'i', 'like', 'chikanz']
