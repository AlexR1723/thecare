import datetime, json, random, hashlib

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from .models import *


# from shop.models import Product


def global_function(request):
    number = Contact.objects.filter(is_main=True, contact_id=2)[0].text
    email = Contact.objects.filter(is_main=True, contact_id=4)[0].text

    basket = 0
    ses = request.session.get(settings.CART_SESSION_ID)
    if ses and ses is not None:
        for i in ses.values():
            basket += int(i['total'])

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
    print(prod_ses)

    all_prices = 0
    if prod_ses is not None:
        for i in prod_ses.values():
            all_prices += int(i['total'])
        # products = Product.objects.filter(slug__in=prod_ses.keys())
        products = ProductSize.objects.filter(id__in=prod_ses.keys())
    return render(request, 'Main/Cart.html', locals())


def session_save(request, obj):
    try:
        request.session[settings.CART_SESSION_ID] = obj
        request.session.modified = True
        return True
    except:
        return False


def session_delete(request, obj):
    try:
        del request.session[obj]
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
    try:
        ses = create_cart_session(request)
        if ses != False:
            count = int(request.GET.get('count'))
            prod_size = int(request.GET.get('prod_size'))
            pr_sz = ProductSize.objects.get(id=int(prod_size))
            item = str(pr_sz.id)
            if item not in ses:
                ses[item] = {'count': count, 'total': pr_sz.price * count}
            else:
                ses[item] = {'count': ses[item]['count'] + count,
                             'total': pr_sz.price * (ses[item]['count'] + count)}
            session_save(request, ses)
            total_price = 0
            print(request.session.get(settings.CART_SESSION_ID))
            for i in request.session.get(settings.CART_SESSION_ID).values():
                total_price += int(i['total'])
            return HttpResponse(json.dumps((total_price)))
        else:
            return HttpResponse(json.dumps((False)))
    except:
        return HttpResponse(json.dumps((False)))


def plus_minus_product(request):
    try:
        ses = create_cart_session(request)
        if ses != False:
            slug = int(request.GET.get('slug'))
            minus = request.GET.get('minus')
            count = request.GET.get('count')
            pr_sz = ProductSize.objects.get(id=int(slug))
            item = str(pr_sz.id)
            if minus:
                print('minus')
                ses[item] = {'count': int(ses[item]['count']) - 1,
                             'total': int(pr_sz.price) * (int(ses[item]['count']) - 1)}
            else:
                if count:
                    print('change')
                    ses[item] = {'count': int(count), 'total': int(pr_sz.price) * int(count)}
                else:
                    print('plus')
                    ses[item] = {'count': int(ses[item]['count']) + 1,
                                 'total': int(pr_sz.price) * (int(ses[item]['count']) + 1)}
            session_save(request, ses)
            total_price = 0
            print(request.session.get(settings.CART_SESSION_ID))
            ses = request.session.get(settings.CART_SESSION_ID)
            for i in ses.values():
                total_price += int(i['total'])
            res = {
                'prod_count': ses[item]['count'],
                'product_total': ses[item]['total'],
                'total': total_price
            }
            return HttpResponse(json.dumps((res)))
        else:
            return HttpResponse(json.dumps((False)))
    except:
        return HttpResponse(json.dumps((False)))


def del_product(request):
    try:
        ses = create_cart_session(request)
        if ses != False:
            slug = int(request.GET.get('slug'))
            pr_sz = ProductSize.objects.get(id=int(slug))
            item = str(pr_sz.id)
            if item in ses:
                del ses[item]
                session_save(request, ses)
            else:
                return HttpResponse(json.dumps((False)))
            total_price = 0
            print(request.session.get(settings.CART_SESSION_ID))
            for i in request.session.get(settings.CART_SESSION_ID).values():
                total_price += int(i['total'])
            return HttpResponse(json.dumps((total_price)))
        else:
            return HttpResponse(json.dumps((False)))
    except:
        return HttpResponse(json.dumps((False)))


def buy_products(request):
    user = get_user_id(request)
    if user:
        ids = ProductSize.objects.all().values_list('id', flat=True)
        # print(ids)
        # print(list(ids))
        random.shuffle(list(ids))
        print(ids)
        us_or = UserOrders(user_id=user, date=datetime.date.today(), status_id=1, summ=55555)
        # us_or.save()
        inc = 0
        for i in range(10):
            item = ids[i]
            count = random.randrange(1, 5)
            order_prods = OrdersProducts(order_id=us_or.id, product_id=item, count=count)
            # order_prods.save()
            inc += 1
            print(inc)
        return HttpResponse(json.dumps(True))
    else:
        return HttpResponse(json.dumps(True))

def confirm_order(request):
    dic = global_function(request)
    fio=request.POST.get('fio')
    address=request.POST.get('address')
    email=request.POST.get('email')
    tel=request.POST.get('tel')
    print(fio,address,email,tel)
    prod_ses = request.session.get(settings.CART_SESSION_ID)
    print(prod_ses)

    all_prices = 0
    if prod_ses is not None:
        for i in prod_ses.values():
            all_prices += int(i['total'])
        # products = Product.objects.filter(slug__in=prod_ses.keys())
        products = ProductSize.objects.filter(id__in=prod_ses.keys())
    return render(request, 'Main/Confirm_order.html', locals())


# записывать заказ в бд
# проверять заказ по номеру
# сверстать страницу оплаты
# создать таблицу в бд с товарами ???
def pay_result(request):
    # $out_summ = $_REQUEST["OutSum"];
    # $inv_id = $_REQUEST["InvId"];
    # $shp_item = $_REQUEST["Shp_item"];
    # $crc = $_REQUEST["SignatureValue"];
    #
    # $crc = strtoupper($crc);
    #
    # $my_crc = strtoupper(md5("$out_summ:$inv_id:$mrh_pass2:Shp_item=$shp_item"));

    # summ=request.GET.get('OutSum')
    summ = '5656556'
    login = request.GET.get('InvId')
    hash = str(request.GET.get('SignatureValue')).upper()
    hs = summ + settings.PAY_INV + settings.PAY_TEST_PASSWORD_2
    new_hash = hashlib.md5(hs.encode()).hexdigest()
    # hash = hashlib.md5(nm.encode())
    # print(settings.PAY_INV)
    print(new_hash)
    print('create_hash')
    print(create_hash(request))
    return HttpResponse(json.dumps('OK'))


def create_hash(request):
    # summ=request.GET.get('OutSum')
    summ = '5656556'
    hs = settings.PAY_LOGIN + ':' + summ + ':' + settings.PAY_INV + ':' + settings.PAY_TEST_PASSWORD_1
    print(hs)
    user=get_user_id(request)
    if user:
        hs+=':user='+str(user)
    else:
        hs+=':user=0'
    print(hs)
    new_hash = hashlib.md5(hs.encode()).hexdigest()
    print(new_hash)
    return True


def pay_success(request):
    return HttpResponse(json.dumps('success'))


def pay_fail(request):
    return HttpResponse(json.dumps('fail'))
