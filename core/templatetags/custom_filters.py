# custom_filters.py
from django import template

register = template.Library()


@register.filter(name="load_service")
def load_service(value):
    if value:
        return value.split("\n")
    return None
