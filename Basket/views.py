from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import xlrd, xlwt, json, re, hashlib
from django.contrib.auth import authenticate, login, logout, hashers
from django.core.validators import validate_email
from django.db import transaction
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from django.conf import settings
# from shop.models import Product
import os


def global_function(request):
    number = Contact.objects.filter(is_main=True, contact_id=2)[0].text
    email = Contact.objects.filter(is_main=True, contact_id=4)[0].text

    basket = 0
    ses = request.session.get(settings.CART_SESSION_ID)
    if ses:
        for i in ses.values():
            basket += int(i['price'])

    result_dict = {
        'number': number,
        'email': email,
        'basket': basket
    }
    return result_dict


def get_user_id(request):
    user = request.session.get('username', False)
    if user:
        try:
            user = AuthUser.objects.get(username=user).id
        except:
            user = False
    return user


# def func_contact():
#     number = Contact.objects.filter(is_main=True, contact_id=2)[0].text
#     email = Contact.objects.filter(is_main=True, contact_id=4)[0].text
#     return number, email


def check_product_exist(request):
    try:
        ses = request.session.get(settings.CART_SESSION_ID)
        # print(ses)
        prod_keys = set(ses.keys())
        prod_bd = Product.objects.all().values_list('slug', flat=True)
        for i in prod_keys:
            if i not in prod_bd:
                # print(i)
                del ses[i]
        session_save(request, ses)
        # print(res)
        return True
    except:
        return False


# Create your views here.
def Cart(request):
    # number, email = func_contact()
    dic = global_function(request)
    prod_ses = request.session.get(settings.CART_SESSION_ID)
    check_product_exist(request)
    print(prod_ses)
    # print(sorted(prod_ses))
    all_prices = 0
    for i in prod_ses.values():
        all_prices += int(i['price'])
    products = Product.objects.filter(slug__in=prod_ses.keys())

    # print(list(prod_ses))
    return render(request, 'Main/Cart.html', locals())


def session_save(request, obj):
    try:
        request.session[settings.CART_SESSION_ID] = obj
        request.session.modified = True
        return True
    except:
        return False


def create_cart_session(request):
    try:
        ses = request.session.get(settings.CART_SESSION_ID)
        if not ses:
            request.session[settings.CART_SESSION_ID] = {}
            return request.session.get(settings.CART_SESSION_ID)
        else:
            return ses
    except:
        return False


def add_product(request):
    try:
        ses = create_cart_session(request)
        if ses != False:
            slug = request.GET.get('slug')
            count = request.GET.get('count')
            minus = request.GET.get('minus')
            is_del = request.GET.get('del')
            is_cart = request.GET.get('is_cart')

            is_plus_minus = False
            if minus or not count:
                is_plus_minus = True
            # print('count')
            # print(count)
            if not count or int(count) < 1:
                # print('count = 1')
                count = 1
            # if int(count)<0:
            #     print(count)
            #     count=int(count)*(-1)
            product = Product.objects.get(slug=slug)
            if slug not in ses:
                ses[slug] = {'count': count, 'price': int(product.price) * int(count)}
            else:
                if is_del:
                    del ses[slug]
                    session_save(request, ses)
                    all_prices = 0
                    for i in request.session.get(settings.CART_SESSION_ID).values():
                        all_prices += int(i['price'])
                    return HttpResponse(json.dumps(all_prices))

                # print(int(product.price))
                # print(int(count))
                if minus:
                    if ses[slug]['count'] > 1:
                        ses[slug]['count'] = int(ses[slug]['count']) - int(count)
                else:
                    # print('here')
                    if is_cart:
                        ses[slug]['count'] = int(count)
                    else:
                        ses[slug]['count'] = int(ses[slug]['count']) + int(count)
                ses[slug]['price'] = int(product.price) * ses[slug]['count']
            session_save(request, ses)
            print('last ses')
            print(request.session.get(settings.CART_SESSION_ID))
            all_prices = 0
            for i in request.session.get(settings.CART_SESSION_ID).values():
                all_prices += int(i['price'])
            if is_plus_minus or is_cart:
                return HttpResponse(json.dumps([request.session.get(settings.CART_SESSION_ID)[slug]['price'],
                                                request.session.get(settings.CART_SESSION_ID)[slug]['count'],
                                                all_prices]))
            else:
                return HttpResponse(json.dumps(all_prices))
        else:
            return HttpResponse(json.dumps(False))
    except:
        return HttpResponse(json.dumps(False))

# def cart_item_plus(request):
#     try:
#         ses = request.session.get(settings.CART_SESSION_ID)
#         if not ses:
#             request.session[settings.CART_SESSION_ID] = {}
#             return request.session.get(settings.CART_SESSION_ID)
#         else:
#             return ses
#     except:
#         return False
