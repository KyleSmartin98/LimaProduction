from django import template
import datetime
from django.urls import get_resolver, resolve, Resolver404

register = template.Library()

@register.filter(expects_localtime=True)
def less_Than_Thirty_Days(value):
    if isinstance(value, datetime.datetime):
        value = value.date()
    delta = value - datetime.date.today()
    return 15 <= delta.days <= 30

@register.filter(expects_localtime=True)
def less_Than_Fifteen_Days(value):
    if isinstance(value, datetime.datetime):
        value = value.date()
    delta = value - datetime.date.today()
    return 3 < delta.days < 15

@register.filter(expects_localtime=True)
def less_Than_Three_Day(value):
    if isinstance(value, datetime.datetime):
        value = value.date()
    delta = value - datetime.date.today()
    return 0 < delta.days <= 3

@register.filter(expects_localtime=True)
def days_Remaining(value):
    if isinstance(value, datetime.datetime):
        value = value.date()
    delta = value - datetime.date.today()
    return str(delta.days) + " " +'day(s)'


@register.filter(expects_localtime=True)
def activeSample(value):
    if isinstance(value, datetime.datetime):
        value = value.date()
    delta = value - datetime.date.today()
    return 0 < delta.days

@register.filter(expects_localtime=True)
def expiredSample(value):
    if isinstance(value, datetime.datetime):
        value = value.date()
    delta = value - datetime.date.today()
    return delta.days <= 0