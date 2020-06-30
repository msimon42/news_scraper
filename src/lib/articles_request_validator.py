from .helper_methods import *

class ArticlesRequestValidator:
    @classmethod
    def validate(cls, data):
        pass

    def __preprocess(self, data):
        try:
            data['keywords']
        except:
            data['keywords'] = ''

        try:
            data['endDate']
        except:
            data['endDate'] =
