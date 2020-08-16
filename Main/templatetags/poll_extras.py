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


# @register.filter
# def get_dict(value, arg):
#     return value[arg]

    

@register.filter
def convert_to_int(value):
    print('convert_to_int')
    print(value)
    print(type(value))
    if value / int(value) != 1:
        return value
    else:
        print('convert')
        print(int(value))
        return int(value)


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


def session_save(request, obj):
    try:
        request.session[settings.CART_SESSION_ID] = obj
        request.session.modified = True
        return True
    except:
        return False


@register.filter
def gf_busket(request):
    basket = 0
    ses = request.session.get(settings.CART_SESSION_ID)
    # print('gf_busket')
    # print(ses)
    if ses and ses is not None:
        ids = []
        for i in ses.keys():
            ids.append(int(i))
            # print(ids)
        if ids:
            prods = ProductSize.objects.filter(id__in=ids)
            # print(prods)
            for i in ids:
                prod = prods.filter(id=i)[0]
                count = ses[str(i)]['count']
                ses[str(i)]['total'] = prod.price * count
                session_save(request,ses)

        for i in ses.values():
            basket += int(i['total'])
    return basket


@register.filter
def gf_count_items(request):
    itm_cnt = 0
    ses = request.session.get(settings.CART_SESSION_ID)
    if ses and ses is not None:
        # ids = []
        # for i in ses.keys():
        #     ids.append(int(i))
        # prods = ProductSize.objects.filter(id__in=ids)
        # for i in ids:
        #     prod = prods.filter(id=i)[0]
        #     count = ses[str(i)]['count']
        #     ses[str(i)]['total'] = prod.price * count

        for i in ses.values():
            itm_cnt += int(i['count'])
    return itm_cnt





# @register.filter
# def get_media(id):
# 	prod=Product.objects.get(id=id)
# 	return prod.main_photo.url




@register.filter
def get_prod_price_format(id):
	prod=int(Product.objects.get(id=id).id)
	sizes = ProductSize.objects.filter(product__id=prod).order_by('size__float_name', 'size__str_name').values('price')
	# return(sizes[0]['price'])
	if len(sizes) > 0:
		sizes=sizes[0]['price']
		return '{:,}'.format(sizes).replace(',', ' ')
	else:
		return 0
            
          
@register.filter
def get_prod_absolute_url(id):
	prod=Product.objects.get(id=id)
	return reverse('Item_card', kwargs={'slug': prod.slug})

@register.filter	
def is_3(elem):
	if elem % 3 == 0:
		return True
	else:
		return False

@register.filter
def last(elem, all_c):
	if elem == all_c:
		return True
	else:
		return False
