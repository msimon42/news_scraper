from datetime import datetime, timedelta
from src.models import *

def n_days_ago(n):
    return (datetime.now() - timedelta(days=n)).strftime('%m-%d-%y')

def remove_null_values(list):
    return [element for element in list if element is not None]

def random_user_agent_header():
    user_agent = UserAgent.random_user_agent()
    return {'User-Agent':user_agent}
