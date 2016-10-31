from django import template

register = template.Library()

@register.filter
def in_category(things, category):
    return things.filter(category=category)

@register.filter
def is_available(things):
    return things.filter(is_available=True)