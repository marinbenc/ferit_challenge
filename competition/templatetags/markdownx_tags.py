from django import template
from markdownx.utils import markdownify
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def markdown(value):
    return mark_safe(markdownify(value))
