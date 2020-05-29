from datetime import datetime, timedelta

def n_days_ago(n):
    return (datetime.now() - timedelta(days=n)).strftime('%m-%d-%y')

def remove_null_values(list):
    return [element for element in list if element is not None]
