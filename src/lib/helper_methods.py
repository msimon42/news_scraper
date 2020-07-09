from datetime import datetime, timedelta

def n_days_ago(n):
    return (datetime.now() - timedelta(days=n)).strftime('%m-%d-%y')

def remove_null_values(list):
    return [element for element in list if element is not None]

def remove_spaces_from_beginning_str(str):
    try:
        while str[0] == ' ':
            str = str[1:]

        return str
    except:
        return str

def today():
    return datetime.now().strftime('%m-%d-%y')

def current_year():
    return datetime.now().year

def convert_to_date(date_string):
    return datetime.strptime(date_string, '%m-%d-%Y')

def convert_to_sql_like(phrase, column):
    return f'{column} LIKE %{phrase}%'    

def do_nothing():
    pass
