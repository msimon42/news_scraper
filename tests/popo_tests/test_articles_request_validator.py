from src.lib.articles_request_validator import ArticlesRequestValidator

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
