from django import template
from time import mktime
from datetime import datetime

register = template.Library()

def getunixtime(datetime):
    return mktime(datetime.timetuple())

def to_timezone(unixtime, timezone):
    print('to_timezone called with %s and %s', unixtime, timezone)
    return datetime.fromtimestamp(int(unixtime), timezone);

register.filter('getunixtime', getunixtime)
register.filter('to_timezone', to_timezone)
