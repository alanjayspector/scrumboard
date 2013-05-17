__author__ = 'alanspector'

import re
import datetime
import pytz


DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def getLocalizeDateTime(date_string, tz):
    utc_dt = datetime.datetime.strptime(date_string, DATE_FORMAT)
    utc_dt = utc_dt.replace(tzinfo=pytz.utc)
    loc_dt = utc_dt.astimezone(tz)
    return loc_dt.strftime(DATE_FORMAT)



def timeZoneChangeExample(dateString):

    easternTZ = pytz.timezone("US/Eastern")
    westernTZ = pytz.timezone("US/Pacific")
    centralTZ = pytz.timezone("US/Central")
    utcTZ = pytz.timezone("UTC")
    print dateString
    print getLocalizeDateTime(dateString, easternTZ)
    print getLocalizeDateTime(dateString, westernTZ)
    print getLocalizeDateTime(dateString, centralTZ)
    print getLocalizeDateTime(dateString, utcTZ)

def toDict(instance):
        ourDict = {}
        for k,v in instance.__dict__.items():
            isAnIDColumn = re.search("__ID$", k)
            if isAnIDColumn:
                continue
            protected_attr_check = re.search("__(\w+)$", k)
            if protected_attr_check:
                groups = protected_attr_check.groups()
                if len(groups) > 1:
                    raise Exception,\
                        "atttribute {} breaks toDict() check _<CLASS>__attribute".format(k)
                ourDict[groups[0]] = v
            else:
                if hasattr(v,"ID"):
                    ourDict[k] = v.ID
                elif isinstance(v, dict):
                    ourDict[k] = v.keys()
                else:
                    ourDict[k] = v
        return ourDict




