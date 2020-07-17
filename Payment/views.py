from django.shortcuts import render
from .models import *

from django.conf import settings
# def global_function(request):
#     number = Contact.objects.filter(is_main=True, contact_id=2)[0].text
#     email = Contact.objects.filter(is_main=True, contact_id=4)[0].text
#
#     ses = request.session.get(settings.CART_SESSION_ID)
#     ids = []
#     for i in ses.keys():
#         ids.append(int(i))
#     prods = ProductSize.objects.filter(id__in=ids)
#     for i in ids:
#         prod = prods.filter(id=i)[0]
#         count = ses[str(i)]['count']
#         ses[str(i)]['total'] = prod.price * count
#
#     basket = 0
#     ses = request.session.get(settings.CART_SESSION_ID)
#     if ses and ses is not None:
#         for i in ses.values():
#             basket += int(i['total'])
#
#     is_auth = request.user.is_authenticated
#     if is_auth:
#         is_auth = request.session.get('username', False)
#
#     user_name = ''
#     if is_auth:
#         user_name = AuthUser.objects.get(username=is_auth).first_name
#
#     result_dict = {
#         'number': number,
#         'email': email,
#         'basket': basket,
#         'is_auth': is_auth,
#         'user_name': user_name
#     }
#     return result_dict


def Payments(request):
    # dic = global_function(request)

    list = Payment.objects.all()
    return render(request, 'Payment/Payment.html', locals())