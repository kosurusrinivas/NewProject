from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='split')
def split(value, arg):
    """Splits a string by a delimiter"""
    return value.split(arg)