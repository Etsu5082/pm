# main_app/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def percentage(current, maximum):
    """
    current / maximum * 100 の計算を行い、パーセンテージを返す。
    """
    try:
        return (current / maximum) * 100
    except (ValueError, ZeroDivisionError):
        return 0
