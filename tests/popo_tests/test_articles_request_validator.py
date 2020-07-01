from src.lib.articles_request_validator import ArticlesRequestValidator
from src.lib.helper_methods import *

class TestArticlesRequestValidator:
    def setup(self):
        validator = ArticlesRequestValidator()

    def test_preprocess(self):
        data_1 = {
            'keywords':'test',
            'startDate':'06-01-2020',
            'endDate':'06-15-2020',
            'amount':10
        }

        data_2 = {
            'startDate':'05-31-2020',
            'amount':15
        }

        data_3 = {
            'keywords':''
        }

        assert self.validator.preprocess(data_1) == {
                                                        'keywords':'test',
                                                        'startDate':'06-01-2020',
                                                        'endDate':'06-15-2020',
                                                        'amount':10
                                                    }

        assert self.validator.preprocess(data_2) == {
                                                        'keywords':'',
                                                        'startDate':'05-31-2020',
                                                        'endDate':today(),
                                                        'amount':15
                                                    }

        assert self.validator.preprocess(data_3) == {
                                                        'keywords':'',
                                                        'startDate':'12-31-2019',
                                                        'endDate':today(),
                                                        'amount':0
                                                    }


        def test_valid_amount(self):
            assert self.validator.valid_amount(12)
            assert not self.validator.valid_amount(3)
            assert not self.validator.valid_amount(187)
            assert self.validator.valid_amount(10)
            assert self.validator.valid_amount(100)


        def test_valid_date(self):
            assert not self.validator.valid_date('12-31-2019')
            assert not self.validator.valid_date('12-31-20200')
            assert not self.validator.valid_date('13-22-2020')
            assert not self.validator.valid_date('08-42-2020')
            assert not self.validator.valid_date('0831-2020')
            assert not self.validator.valid_date('08312020')
            assert self.validator.valid_date('06-30-2020')
            assert self.validator.valid_date('07-14-2020')   
