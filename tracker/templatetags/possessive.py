from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='possessive')
@stringfilter
def possessive(string):
    if string[-2:] == "'s" or string[-2:] == "’s":
        return string
    elif string[-1:] == "s":
        return f"{string}’"
    else:
        return f"{string}’s"
