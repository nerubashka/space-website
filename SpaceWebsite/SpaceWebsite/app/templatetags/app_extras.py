from django import template

register = template.Library()


@register.filter(name='font_default')
def font_default(value):
    return value.replace("font-family: 'Helvetica Neue', Arial, 'Liberation Sans', FreeSans, sans-serif;"," ")
