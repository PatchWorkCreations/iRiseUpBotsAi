# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def add_one(value):
    return value + 1

@register.filter
def replace(value, args):
    """
    Replace all instances of `old` with `new` in the string.
    `args` should be a string with the old and new values separated by a comma.
    Example: {{ value|replace:"old,new" }}
    """
    old, new = args.split(',')
    return value.replace(old, new)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    return value.as_widget(attrs={"class": css_class})
