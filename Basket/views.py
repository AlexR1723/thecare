from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import xlrd, xlwt, json, re, hashlib,random,datetime
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
    if ses and ses is not None:
        for i in ses.values():
            basket += int(i['price'])

    is_auth = request.user.is_authenticated
    if is_auth:
        is_auth = request.session.get('username', False)

    user_name = ''
    if is_auth:
        user_name = AuthUser.objects.get(username=is_auth).first_name

    result_dict = {
        'number': number,
        'email': email,
        'basket': basket,
        'is_auth': is_auth,
        'user_name': user_name
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
    dic = global_function(request)
    prod_ses = request.session.get(settings.CART_SESSION_ID)
    check_product_exist(request)



    # inc=0
    # prods=Product.objects.all()
    # for i in prods:
    #     i.price=random.randrange(500,12000,10)
    #     i.main_photo='uploads/test_7.png'
    #     i.save()
    #     inc+=1
    #     print(inc)

    all_prices = 0
    if prod_ses is not None:
        for i in prod_ses.values():
            all_prices += int(i['price'])
        products = Product.objects.filter(slug__in=prod_ses.keys())
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
            print('not ses')
            request.session[settings.CART_SESSION_ID] = {}
            # print(request.session.get(settings.CART_SESSION_ID))
            return request.session.get(settings.CART_SESSION_ID)
        else:
            return ses
    except:
        return False


def add_product(request):
    # try:
    ses = create_cart_session(request)
    if ses != False:
        slug = request.GET.get('slug')
        count = request.GET.get('count')
        minus = request.GET.get('minus')
        is_del = request.GET.get('del')
        is_cart = request.GET.get('is_cart')
        size_id = request.GET.get('size_id')

        is_plus_minus = False
        if minus or not count:
            is_plus_minus = True
        if not count or int(count) < 1:
            count = 1
        product = Product.objects.get(slug=slug)
        # print(product.price)
        # print(count)
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

            if minus:
                if ses[slug]['count'] > 1:
                    ses[slug]['count'] = int(ses[slug]['count']) - int(count)
            else:
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
    # except:
    #     return HttpResponse(json.dumps(False))

def buy_products(request):
    user=get_user_id(request)
    if user:
        ids=ProductSize.objects.all().values_list('id',flat=True)
        # print(ids)
        # print(list(ids))
        random.shuffle(list(ids))
        print(ids)
        us_or=UserOrders(user_id=user,date=datetime.date.today(),status_id=1,summ=55555)
        # us_or.save()
        inc=0
        for i in range(10):
            item=ids[i]
            count=random.randrange(1,5)
            order_prods=OrdersProducts(order_id=us_or.id,product_id=item,count=count)
            # order_prods.save()
            inc+=1
            print(inc)
        return HttpResponse(json.dumps(True))
    else:
        return HttpResponse(json.dumps(True))