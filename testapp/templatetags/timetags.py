from django import template
from time import mktime

register = template.Library()

def getunixtime(datetime):
    return mktime(datetime.timetuple())

register.filter('getunixtime', getunixtime)
