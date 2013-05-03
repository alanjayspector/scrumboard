__author__ = 'alanspector'

import datetime
import pytz


DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def getLocalizeDateTime(date_string, tz):
    utc_dt = datetime.datetime.strptime(date_string, DATE_FORMAT)
    utc_dt = utc_dt.replace(tzinfo=pytz.utc)
    loc_dt = utc_dt.astimezone(tz)
    return loc_dt.strftime(DATE_FORMAT)

def getNumberOfHoursBasedUponDates(startDate,EndDate, hoursPerDay) :
    pass

def getRawInput(menu):
    pass

