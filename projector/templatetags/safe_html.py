from django import template

register = template.Library()

@register.filter
def unscript(s):
    return s.replace('<script', '&lt;script')