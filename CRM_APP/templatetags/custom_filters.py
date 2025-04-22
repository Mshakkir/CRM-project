from django import template

register = template.Library()

@register.filter
def replace_spaces(value):
    """
    Custom filter to replace spaces with hyphens.
    """
    if isinstance(value, str):
        return value.replace(" ", "-").lower()
    return value