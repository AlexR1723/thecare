from django import template
from django.conf import settings
from ..models import *

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


@register.filter
def global_function(request):
    # number = Contact.objects.filter(is_main=True, contact_id=2)[0].text
    # email = Contact.objects.filter(is_main=True, contact_id=4)[0].text

    ses = request.session.get(settings.CART_SESSION_ID)
    ids = []
    if ses and ses is not None:
        for i in ses.keys():
            ids.append(int(i))
        prods = ProductSize.objects.filter(id__in=ids)
        for i in ids:
            prod = prods.filter(id=i)[0]
            count = ses[str(i)]['count']
            ses[str(i)]['total'] = prod.price * count

    # basket = 0
    # ses = request.session.get(settings.CART_SESSION_ID)
    # if ses and ses is not None:
    #     for i in ses.values():
    #         basket += int(i['total'])

    # is_auth = request.user.is_authenticated
    # if is_auth:
    #     is_auth = request.session.get('username', False)
    #
    # user_name = ''
    # if is_auth:
    #     user_name = AuthUser.objects.get(username=is_auth).first_name

    # result_dict = {
    #     'number': number,
    #     'email': email,
    #     'basket': basket,
    #     'is_auth': is_auth,
    #     'user_name': user_name
    # }
    # return result_dict



@register.filter
def gf_number(request):
    number = Contact.objects.filter(is_main=True, contact_id=2)[0].text
    return number

@register.filter
def gf_email(request):
    email = Contact.objects.filter(is_main=True, contact_id=4)[0].text
    return email


@register.filter
def gf_user(request):
    is_auth = request.user.is_authenticated
    if is_auth:
        is_auth = request.session.get('username', False)
    user_name = False
    if is_auth:
        user_name = AuthUser.objects.get(username=is_auth).first_name
    return user_name


@register.filter
def gf_busket(request):
    basket = 0
    ses = request.session.get(settings.CART_SESSION_ID)
    if ses and ses is not None:

        ids = []
        for i in ses.keys():
            ids.append(int(i))
        prods = ProductSize.objects.filter(id__in=ids)
        for i in ids:
            prod = prods.filter(id=i)[0]
            count = ses[str(i)]['count']
            ses[str(i)]['total'] = prod.price * count

        for i in ses.values():
            basket += int(i['total'])
    return basket


# @register.filter
# def gf_price_research(request):
#     ses = request.session.get(settings.CART_SESSION_ID)
#     ids = []
#     if ses and ses is not None:
#         for i in ses.keys():
#             ids.append(int(i))
#         prods = ProductSize.objects.filter(id__in=ids)
#         for i in ids:
#             prod = prods.filter(id=i)[0]
#             count = ses[str(i)]['count']
#             ses[str(i)]['total'] = prod.price * count