from django import template

register = template.Library()

@register.filter
def is_priority(arg):
    return arg.item_is_priority

@register.filter
def is_purchased(arg):
    return arg.item_purchased