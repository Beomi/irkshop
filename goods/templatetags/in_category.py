from django import template

register = template.Library()

@register.filter
def in_category(things, category):
    return things.filter(category=category)

@register.filter
def is_available(things):
    if things.is_available:
        return things
    else:
        return None