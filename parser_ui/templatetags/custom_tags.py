__author__ = 'keyvan'

import string
import random

from django import template


register = template.Library()


@register.filter
def indexed(seq):
    return enumerate(seq, start=1)


@register.simple_tag
def random_url_parameter(size=20):
    return '?x=' + ''.join(random.choice(string.ascii_letters) for x in range(size))
