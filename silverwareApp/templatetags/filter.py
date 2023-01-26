from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter(name='dayBefore')
def dayBefore(day):
    return (datetime.today() - day).days

@register.filter(name='mult')
def mult(value, arg):
    return str(int(value) * float(arg))