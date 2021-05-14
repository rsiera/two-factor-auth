from datetime import datetime

STORE_DATETIME_FORMAT = '%B %d %Y %H:%M:%S'
INPUT_STORE_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
INPUT_STORE_DATE_FORMAT = '%Y-%m-%d'
STORE_DATE_FORMAT = '%B %d %Y'


def format_date(date_value):
    _date = datetime.strptime(date_value, INPUT_STORE_DATE_FORMAT)
    return _date.strftime(STORE_DATE_FORMAT)


def format_datetime(datetime_value):
    _datetime = datetime.strptime(datetime_value, INPUT_STORE_DATETIME_FORMAT)
    return _datetime.strftime(STORE_DATETIME_FORMAT)
