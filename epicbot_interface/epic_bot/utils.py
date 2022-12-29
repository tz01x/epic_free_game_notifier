import datetime

DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.000Z"


def get_date_obj(date):
    return datetime.datetime.strptime(date, DATE_TIME_FORMAT)
