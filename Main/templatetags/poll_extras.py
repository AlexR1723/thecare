from django import template

register = template.Library()


@register.filter
def get_prod_count(dic, item):
    return dic[str(item)]['count']


@register.filter
def get_prod_price(dic, item):
    return dic[str(item)]['total']

@register.filter
def make_search_url(value, arg):
    return arg+'='+str(value)

@register.filter
def get_dict(value, arg):
    return value[arg]