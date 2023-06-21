import locale

from django import template

register = template.Library()


@register.filter
def convertWon(number):
    if number:
        locale.setlocale(locale.LC_ALL, 'ko_KR')
        return locale.currency(number, grouping=True).replace("\\", '') + " 원"
    else:
        return "0 원"


@register.filter
def convertDate(date):
    return date.strftime("%Y-%m-%d")


@register.filter
def convertDateTime(date):
    return date.strftime("%Y-%m-%d %H:%M:%S")