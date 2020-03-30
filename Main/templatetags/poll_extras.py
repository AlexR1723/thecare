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
    return arg + '=' + str(value)


@register.filter
def get_dict(value, arg):
    return value[arg]


@register.filter
def convert_to_int(value):
    print(value)
    print(type(value))
    if value / int(value) != 1:
        return value
    else:
        print('convert')
        print(int(value))
        return int(value)
