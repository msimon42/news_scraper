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
