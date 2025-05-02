from django import template

register = template.Library()

@register.filter
def sub(value, arg):
    """Subtract the arg from the value"""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def get_item(dictionary, key):
    """Gets an item from a dictionary safely."""
    return dictionary.get(key, 0)

@register.filter
def peso_format(value):
    """Format a number as peso currency."""
    try:
        value = float(value)
        if value < 0:
            return "-₱{:,.2f}".format(abs(value))
        return "₱{:,.2f}".format(value)
    except (ValueError, TypeError):
        return value
