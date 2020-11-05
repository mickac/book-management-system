from django import template

register = template.Library()


@register.simple_tag
def create_list(*args):
    """Creating list from given arguments."""
    return args
