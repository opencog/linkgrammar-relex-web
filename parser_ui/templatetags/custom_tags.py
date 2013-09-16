__author__ = 'keyvan'

from django import template

register = template.Library()


@register.filter
def indexed(seq):
    return enumerate(seq, start=1)
