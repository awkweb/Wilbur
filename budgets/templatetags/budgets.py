from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.filter()
def rev(value):
    return reverse(value)