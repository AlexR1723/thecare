from django import template
register = template.Library()

@register.filter
def make_search_url(value, arg):
    """Removes all values of arg from the given string"""
    res=arg+'='+str(value)
    return res