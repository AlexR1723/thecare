import datetime, json, random, hashlib

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.db import transaction
from pysendpulse.pysendpulse import PySendPulse
from .models import *


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
    prod_ses = request.session.get(settings.CART_SESSION_ID)
    print(prod_ses)

    # all_prices = 0
    if prod_ses is not None:
        # for i in prod_ses.values():
        # all_prices += int(i['total'])
        # products = Product.objects.filter(slug__in=prod_ses.keys())
        products = ProductSize.objects.filter(id__in=prod_ses.keys())
    if request.user.is_authenticated:
        user_id=get_user_id(request)
        auth_user=AuthUser.objects.get(id=user_id)
        user=Users.objects.get(user=user_id)
        fio=auth_user.last_name+' '+auth_user.first_name+' '+user.patronymic
        adress=user.adress
        phone=user.phone
        email=auth_user.email

    # prods=ProductSize.objects.all()
    # for i in prods:
    #     i.price=random.randrange(1000,15000,50)
    #     i.count=random.randrange(5,23)
    #     sl=random.randrange(1,100)
    #     i.sale=0
    #     i.old_price=0
    #     if sl<40:
    #         i.sale=random.randrange(5,40)
    #         print(i.sale)
    #         print(i.price*(i.sale/100))
    #         print(i.price-i.price*(i.sale/100))
    #         print(i.price)
    #         i.old_price=i.price-i.price*(i.sale/100)
    #         print('------------')
    #     i.save()
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
            cnt = 0
            for i in request.session.get(settings.CART_SESSION_ID).values():
                total_price += int(i['total'])
                cnt += int(i['count'])
            return HttpResponse(json.dumps([total_price, cnt]))
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
            cnt = 0
            for i in ses.values():
                total_price += int(i['total'])
                cnt += int(i['count'])
            res = {
                'prod_count': ses[item]['count'],
                'product_total': ses[item]['total'],
                'total': total_price,
                'cnt': cnt
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
            cnt = 0
            for i in request.session.get(settings.CART_SESSION_ID).values():
                total_price += int(i['total'])
                cnt += int(i['count'])
            return HttpResponse(json.dumps([total_price, cnt]))
        else:
            return HttpResponse(json.dumps((False)))
    except:
        return HttpResponse(json.dumps((False)))


# @transaction.atomic()
# def buy_products(request):
#     prod_ses = request.session.get(settings.CART_SESSION_ID)
#     # print(prod_ses)
#     # print(list(prod_ses.keys()))
#     ids = []
#     for i in prod_ses.keys():
#         ids.append(int(i))
#
#     summ = 0
#     prods = ProductSize.objects.filter(id__in=ids)
#     for i in ids:
#         prod = prods.filter(id=i)[0]
#         count = prod_ses[str(i)]['count']
#         summ+= prod.price * count
#
#     with transaction.atomic():
#         inv = int(UserOrders.objects.latest('order_number').order_number)+1
#         new_user_order=UserOrders(order_number=inv)
#         # nhash=str(datetime.datetime.now())
#         new_user_order.save()
#         # print('inv')
#         # print(inv)
#         # hs=""
#         hs = settings.PAY_LOGIN + ':' + str(summ) + ':' + str(inv) + ':' + settings.PAY_TEST_PASSWORD_1
#         # print(hs)
#         user = get_user_id(request)
#         # if user:
#         #     hs += ':user=' + str(user)
#         # else:
#         #     hs += ':user=0'
#         # print(hs)
#         # new_hash = hashlib.md5(hs.encode()).hexdigest()
#         # print(new_hash)
#         # dct={}
#         # dct['login']=settings.PAY_LOGIN
#         # dct['signature']=new_hash
#         # dct['outsumm']=summ
#         # dct['inv']=inv
#         # dct['desc']='description'
#         # dct['user']=str(int(user))
#         # MerchantLogin=settings.PAY_LOGIN
#         # OutSum=summ
#
#
#         # mrh_login = "Test1999";
#     # $mrh_pass1 = "password_1";
#     # $inv_id = 678678;
#     # $inv_desc = "Товары для животных";
#     # $out_summ = "100.00";
#     # $IsTest = 1;
#     # $crc = md5("$mrh_login:$out_summ:$inv_id:$mrh_pass1");
#
#     # for i in ids:
#     #     prod = prods.filter(id=i)[0]
#     #     count = ses[str(i)]['count']
#     #     ses[str(i)]['total'] = prod.price * count
#
#     # all_prices = 0
#     # if prod_ses is not None:
#     #     for i in prod_ses.values():
#     #         all_prices += int(i['total'])
#     #     # products = Product.objects.filter(slug__in=prod_ses.keys())
#     #     products = ProductSize.objects.filter(id__in=prod_ses.keys())
#     if user:
#         # ids = ProductSize.objects.all().values_list('id', flat=True)
#         # # print(ids)
#         # # print(list(ids))
#         # random.shuffle(list(ids))
#         # print(ids)
#         # us_or = UserOrders(user_id=user, date=datetime.date.today(), status_id=1, summ=55555)
#         # # us_or.save()
#         # inc = 0
#         # for i in range(10):
#         #     item = ids[i]
#         #     count = random.randrange(1, 5)
#         #     order_prods = OrdersProducts(order_id=us_or.id, product_id=item, count=count)
#         #     # order_prods.save()
#         #     inc += 1
#         #     print(inc)
#         return HttpResponse(json.dumps(True))
#     else:
#         return HttpResponse(json.dumps(True))

def confirm_order(request):
    # dic = global_function(request)
    fio = request.POST.get('fio')
    address = request.POST.get('address')
    email = request.POST.get('email')
    tel = request.POST.get('tel')
    print(fio, address, email, tel)
    prod_ses = request.session.get(settings.CART_SESSION_ID)
    print(prod_ses)

    all_prices = 0
    ids = []
    print('prod_ses')
    print(prod_ses)
    if prod_ses is not None:
        products = ProductSize.objects.filter(id__in=prod_ses.keys())
        for i in products:
            count = prod_ses[str(i.id)]['count']
            all_prices += i.price * count
        print(products)

    ses = request.session.get(settings.CART_USER)
    if not ses:
        request.session[settings.CART_USER] = {}
        ses = request.session.get(settings.CART_USER)
    ses['fio'] = str(fio).strip()
    ses['address'] = str(address).strip()
    ses['phonenumber'] = str(tel).strip()
    ses['email'] = str(email).strip()

    return render(request, 'Main/Confirm_order.html', locals())


# записывать заказ в бд
# проверять заказ по номеру
# создать таблицу в бд с товарами оплаченными ???
# проверять количество заказываемого товара с количеством на складе
def pay_result(request):
    print('pay_result')
    OutSum = request.GET.get('OutSum')
    InvId = request.GET.get('InvId')
    SignatureValue = request.GET.get('SignatureValue')
    Shp_User = request.GET.get('Shp_User')
    hs = str(OutSum) + ':' + str(InvId) + ':' + settings.PAY_PASSWORD_2 + ':Shp_User=' + str(Shp_User)
    new_hash = hashlib.md5(hs.encode()).hexdigest()
    print(new_hash)
    print(SignatureValue)
    if str(SignatureValue).lower() == str(new_hash).lower():

        # отправка не больше десяти писем в секунду
        print('send mail')
        SPApiProxy = PySendPulse(settings.EMAIL_REST_API_ID, settings.EMAIL_REST_API_SECRET, 'memcached')
        email = {
            'subject': 'Уведомление от системы',
            'html': '<h1>Hello, Anastason!</h1><p>This message is only sent to very pretty girls!</p>',
            'text': ' пр Проверка рабоспособности почты',
            'from': {'name': 'The Care', 'email': 'mail@thecare.ru'},
            'to': [
                {'name': 'Anastason', 'email': 'leha.avdeenko.98@mail.ru'}
            ]
        }
        # sending = SPApiProxy.smtp_send_mail(email)
        # print(sending)

        order = UserOrders.objects.filter(order_number=InvId)[0]
        order.status_id = 1
        order.date = datetime.datetime.now()
        order.save()
        prods = UserOrderProducts.objects.filter(order_id=order.id)
        for i in prods:
            prod = ProductSize.objects.get(id=i.product_size_id)
            print('prod')
            print(prod.count)
            print(i.count)
            cnt = prod.count - i.count
            print(cnt)
            if cnt < 0:
                print('less 0')
                session_save(request, {})
                return HttpResponse(json.dumps('bad sign'))
            else:
                prod.count = cnt
                prod.save()
                print('count after order' + str(prod.count))
        return HttpResponse(json.dumps('OK' + str(InvId)))
    else:
        return HttpResponse(json.dumps('bad sign'))


def pay_success(request):
    # return HttpResponse(json.dumps('success'))
    OutSum = request.GET.get('OutSum')
    InvId = request.GET.get('InvId')
    return render(request, 'success.html', locals())


def pay_fail(request):
    # return HttpResponse(json.dumps('fail'))
    return render(request, 'fail.html', locals())


def pay_check(request):
    user = get_user_id(request)
    if not user:
        user = 0
    print(user)
    prod_ses = request.session.get(settings.CART_SESSION_ID)
    print(prod_ses)
    ids = []
    for i in prod_ses.keys():
        ids.append(int(i))
    summ = 0
    prods = ProductSize.objects.filter(id__in=ids)
    for i in ids:
        prod = prods.filter(id=i)[0]
        count = prod_ses[str(i)]['count']
        summ += prod.price * count
    ses_user = request.session.get(settings.CART_USER)
    with transaction.atomic():
        inv = int(UserOrders.objects.latest('order_number').order_number) + 1
        us_ord = UserOrders(amount=summ, status_id=4, order_number=inv, fio=ses_user['fio'],
                            phonenumber=ses_user['phonenumber'], address=ses_user['address'],
                            email=ses_user['email'])
        if user:
            us_ord.user_id = user
        us_ord.save()
        print(prods)
        for i in prods:
            uop = UserOrderProducts(order_id=us_ord.id, product_size_id=i.id, count=int(prod_ses[str(i.id)]['count']),
                                    amount=i.price)
            uop.save()
        hs = settings.PAY_LOGIN + ':' + str(summ) + ':' + str(
            us_ord.order_number) + ':' + settings.PAY_PASSWORD_1 + ':Shp_User=' + str(user)
        # hs = settings.PAY_LOGIN + ':' + str(summ) + ':' + str(us_ord.order_number) + ':' + settings.PAY_TEST_PASSWORD_1
        print(hs)
        new_hash = hashlib.md5(hs.encode()).hexdigest()
        print(new_hash)

        # ses = request.session.get(settings.CART_ORDER_NUMBER)
        # if not ses:
        #     print('not ses')
        #     ses=request.session[settings.CART_ORDER_NUMBER] = {}
        # ses['order_number']=us_ord.order_number
        # print(ses.keys())

        dc = {}
        dc['SignatureValue'] = new_hash
        dc['OutSum'] = str(summ)
        dc['Shp_user'] = user
        dc['MerchantLogin'] = settings.PAY_LOGIN
        dc['InvoiceID'] = us_ord.order_number
        return HttpResponse(json.dumps(dc))


def send_mail(request):

    return HttpResponse(json.dumps(True))
