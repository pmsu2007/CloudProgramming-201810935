import locale
import math

from django import template

register = template.Library()


@register.filter
def convertWon(number):
    locale.setlocale(locale.LC_ALL, 'ko_KR')
    return locale.currency(number, grouping=True).replace("\\", '') + " 원"


@register.filter
def convertPercentage(amount, balance):
    result = balance / amount
    if result >= 1:
        return round(result, 1)
    else:
        return round(result * 100, 1)
