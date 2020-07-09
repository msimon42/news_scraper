from .helper_methods import *

class ArticlesRequestValidator:
    def __init__(self):
        pass

    @classmethod
    def validate(cls, data):
        validator = cls()
        preprocessed_data = validator.preprocess(data)

        all_checks_valid = all([
            validator.valid_amount(data['amount']),
            validator.valid_date(data['startDate']),
            validator.valid_date(data['endDate']),
        ])

        if all_checks_valid:
            return preprocessed_data


    def preprocess(self, data):
        valid_keys = ['keywords', 'endDate', 'startDate', 'amount']

        data.setdefault('keywords', '')
        data.setdefault('endDate', today())
        data.setdefault('startDate', '12-31-2019')
        data.setdefault('amount', 0)

        for k in data:
            if k not in valid_keys:
                data[k] = None

        return data

    def postprocess(self, data):
        data['keywords'] = data['keywords'].split(',')
        return data    

    def valid_amount(self, data):
        return data >= 10 and data <= 100

    def valid_date(self, data):
        contains_dashes = '-' in data
        values = data.split('-')
        proper_format = len(values)==3

        try:
            valid_month = (int(values[0]) > 0 and int(values[0]) <= 12)
            valid_day = (int(values[1]) > 0 and int(values[1]) <= 31)
            valid_year = (int(values[2]) >= 2020 and int(values[2]) <= int(current_year()))
        except:
            return False

        return all([contains_dashes, proper_format, valid_month, valid_day, valid_year])

    def proper_date_input(self, start_date, end_date):
        return convert_to_date(start_date) <= convert_to_date(end_date)
