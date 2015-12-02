__author__ = 'sunary'


from datetime import datetime, timedelta


def name_append_date(name):
    today = datetime.today()
    return today.strftime(name + '_' + '%Y%m%d')

def timestamp_previous_days(days=0):
    previous_days = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days, hours=0)
    return previous_days.strftime('%Y-%m-%d 00-00-00')

def iso_previous_days(days=0):
    previous_days = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days, hours=0)
    return previous_days.isoformat()

def date_previous_days(days=0):
    previous_days = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days, hours=0)
    return previous_days.strftime('%Y-%m-%d')

def object_id_previous_days(days=0):
    from bson.objectid import ObjectId

    return ObjectId.from_datetime(datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days, hours=0))

def date_range_of_weekth(week, year):
    '''
    Examples:
        >>> date_range_of_weekth(25, 2015)
        (datetime.datetime(2015, 6, 15, 0, 0), datetime.datetime(2015, 6, 21, 23, 59, 59, 999999))
    '''
    start_first_week = datetime(year, 1, 1)
    if(start_first_week.weekday() > 3):
        start_first_week = start_first_week + timedelta(7 - start_first_week.weekday())
    else:
        start_first_week = start_first_week - timedelta(start_first_week.weekday())
    date_delta = timedelta(days=(week - 1) * 7)
    return (start_first_week + date_delta, start_first_week + date_delta + timedelta(days=7) - timedelta(microseconds=1))

def daterange(start_date, end_date):
    for i in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(i)

if __name__ == '__main__':
    import doctest
    doctest.testmod()