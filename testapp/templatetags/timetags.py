from django import template
from time import mktime
import datetime
import pytz

register = template.Library()

def getunixtime(datetime):
    return mktime(datetime.timetuple())

def to_timezone(unixtime, timezone):
    usertime = timezone.fromutc(datetime.datetime.fromtimestamp(unixtime))
    return usertime.strftime('%Y %b %d %I:%M %p')

register.filter('getunixtime', getunixtime)
register.filter('to_timezone', to_timezone)
