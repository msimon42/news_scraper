from .helper_methods import *

class ArticlesRequestValidator:
    def __init__(self):
        pass
        
    @classmethod
    def validate(cls, data):
        validator = cls()
        preprocessed_data = validator.__preprocess(data)

    def __preprocess(self, data):
        try:
            data['keywords']
        except:
            data['keywords'] = ''

        try:
            data['endDate']
        except:
            data['endDate'] = today()

        return data
