from datetime import datetime, timedelta

def n_days_ago(n):
    return (datetime.now() - timedelta(days=n)).strftime('%m-%d-%y')

def remove_null_values(list):
    return [element for element in list if element is not None]

def random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6',
        'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'

    ]
