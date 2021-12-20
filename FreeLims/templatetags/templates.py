from django import template
import datetime

register = template.Library()

@register.filter(expects_localtime=True)
def less_Than_Thirty_Days(value):
    #value = datetime.datetime.strptime(value, '%Y-%m-%d')
    if isinstance(value, datetime.datetime):
        value = value.date()
    delta = value - datetime.date.today()
    return 15 <= delta.days <= 30

@register.filter(expects_localtime=True)
def less_Than_Fifteen_Days(value):
    #value = datetime.datetime.strptime(value, '%Y-%m-%d')
    if isinstance(value, datetime.datetime):
        value = value.date()
    delta = value - datetime.date.today()
    return 3 < delta.days < 15

@register.filter(expects_localtime=True)
def less_Than_Three_Day(value):
    #value = datetime.datetime.strptime(value, '%Y-%m-%d')
    if isinstance(value, datetime.datetime):
        value = value.date()
    delta = value - datetime.date.today()
    return 0 < delta.days <= 3

@register.filter(expects_localtime=True)
def days_Remaining(value):
    #value = datetime.datetime.strptime(value, '%Y-%m-%d')
    if isinstance(value, datetime.datetime):
        value = value.date()
    delta = value - datetime.date.today()
    return str(delta.days) + " " +'day(s)'