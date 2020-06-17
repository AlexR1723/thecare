from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import xlrd, xlwt, json, re, hashlib, random
from django.contrib.auth import authenticate, login, logout, hashers
from django.core.validators import validate_email
from django.db import transaction
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import Http404
from django.core.files.storage import default_storage
from openpyxl import load_workbook

import os
from django.conf import settings

list=[]
list_count=0

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
    # print('user')
    # print(user)
    return user


def Main(request):
    # print(request.session.get('username', False))
    # inc=0;
    # pr=Product.objects.all()
    # for i in pr:
    #     i.main_photo='uploads/test_7.png'
    #     i.price=random.randrange(100,20000,10)
    #     i.artikul=random.randrange(11111111,99999999)
    #     i.count=random.randrange(1,100)
    #     i.save()
    #     inc+=1
    #     print(inc)

    dic = global_function(request)
    slide_first = Slider.objects.all()[0]
    slide = Slider.objects.all()[1:]
    main_block = MainBlock.objects.all()
    face_count = Product.objects.order_by('-id').filter(category__name='Для лица').count()
    if face_count < 10:
        face = Product.objects.order_by('-id').filter(category__name='Для лица')
    else:
        face = Product.objects.order_by('-id').filter(category__name='Для лица')[0:10]
    # print(face)
    hair_count = Product.objects.order_by('-id').filter(category__name='Для волос').count()
    if hair_count < 10:
        hair = Product.objects.order_by('-id').filter(category__name='Для волос')
    else:
        hair = Product.objects.order_by('-id').filter(category__name='Для волос')[0:10]
    # print(hair)
    body_count = Product.objects.order_by('-id').filter(category__name='Для тела').count()
    if body_count < 10:
        body = Product.objects.order_by('-id').filter(category__name='Для тела')
    else:
        body = Product.objects.order_by('-id').filter(category__name='Для тела')[0:10]
    # print(body)
    # k=0
    # if k == 0:
    #     raise Http404
    return render(request, 'Main/Main.html', locals())


def Dev(request):
    dic = global_function(request)
    return render(request, 'Main/Dev.html', locals())

def Save_excel_file(request):
    print('Save_excel_file')
    if request.method == 'POST':
        doc = request.FILES
        if (doc):
            settings.DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
            print(doc['excel-file'])
            file = Files(file=doc['excel-file'])
            file.save()
            print(file.file.path)
            rb = xlrd.open_workbook(file.file.path)
            # rb = xlrd.open_workbook(default_storage.location + file.file.name)
            # url = default_storage.url(file.file.name)
            # rb = xlrd.open_workbook(settings.MEDIA_ROOT + '/' + file.file.name)
            # print(settings.MEDIA_ROOT + '/' + file.file.name)
            # wb = load_workbook(settings.MEDIA_ROOT + '/' + file.file.name)
            # rb = xlrd.open_workbook(url)
            sheet = rb.sheet_by_index(0)
            vals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]
            for v in vals:
                try:
                    # print('----------------------------------------------------------------------------')
                    # print(v)
                    list.append(v)

                except:
                    print('ex1')
            settings.DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
            list_count=len(list)
            print(list_count)
    return HttpResponseRedirect("/admin")


def get_product_count(request):
    return HttpResponse(json.dumps(len(list)))

def save_product(request):
    print('save_product')
    i=int(request.GET.get('i'))
    print('-----------------------------------')
    v=list[i]
    print(v)
    if v[1] != "" and v[1] != "Привязка к позиции":
        categ = CategoryType.objects.filter(name=v[8])
        print(categ)
        res = ResourceType.objects.filter(category=categ[0]).filter(name=v[9])
        if res.count() == 0:
            res = ResourceType(category=categ[0], name=v[9])
            res.save()
            res = ResourceType.objects.filter(category=categ[0]).filter(name=v[9])
        print(res)
        brand = Brands_model.objects.filter(name__iexact=v[2])
        if brand.count() == 0:
            brand = Brands_model(name=v[2])
            brand.save()
        else:
            brand = Brands_model.objects.get(name=v[2])
        print(brand)
        product = Product.objects.filter(title=v[3]).filter(brand__name=v[2]).filter(
            shot_description=v[4])
        print(product)
        if categ.count() > 0 and res.count() > 0:
            if product.count() == 0:
                print(1)
                product_str = Product_str(title=v[3], shot_description=v[4], description=v[5], note=v[6],
                                  components=v[7],
                                  category=categ[0], resource=res[0], brand=brand, artikul=v[14],
                                  artik_brand=v[15], main_photo="uploads/product/" +v[11])
                product_str.save()
                product=Product.objects.get(id=product_str.id)
            else:
                product = product[0]
                product.description = v[5]
                product.note = v[6]
                product.components = v[7]
                product.category = categ[0]
                product.resource = res[0]
                product.brand = brand
                product.artikul = v[14]
                product.artik_brand = v[15]
                product.main_photo="uploads/product/" +v[11]
                product.save()

            needs = v[10]
            list_need = needs.split(', ')
            print(list_need)
            if len(list_need) == 1:
                need = NeedType.objects.filter(name__iexact=needs).filter(category=categ[0])
                print(need)
                if need.count() == 0:
                    need = NeedType(name=needs, category=categ[0])
                    need.save()
                    need = NeedType.objects.filter(name=needs).filter(category=categ[0])
                print(need[0])
                product_need = ProductNeed.objects.filter(product=product).filter(need=need[0])
                if product_need.count() == 0:
                    product_need = ProductNeed(product=product, need=need[0])
                    product_need.save()
            else:
                for n in list_need:
                    need = NeedType.objects.filter(name_iexact=n).filter(category=categ[0])
                    print(need)
                    if need.count() == 0:
                        need = NeedType(name=n, category=categ[0])
                        need.save()
                        need = NeedType.objects.filter(name=n).filter(category=categ[0])
                    print(need)
                    product_need = ProductNeed.objects.filter(need=need[0]).filter(product=product)
                    if product_need.count() == 0:
                        product_need = ProductNeed(product=product, need=need[0])
                        product_need.save()

            if v[13] != "" and v[13] != " ":
                tones = v[13]
                list_tone = tones.split('; ')
                if list_tone != "" and list_tone.count != 0:
                    for t in list_tone:
                        product_tone = ProductTone(product=product, name=t)
                        product_tone.save()
            if v[12] == "":
                size_name = 0
            else:
                size_name = v[12]
            print(size_name)
            try:
                size_name = float(size_name)
                size = Size.objects.filter(float_name=size_name)
                if size.count() == 0:
                    size = Size(float_name=size_name)
                    size.save()
                else:
                    size = size[0]
            except:
                size = Size.objects.filter(str_name=size_name)
                if size.count() == 0:
                    size = Size(str_name=size_name)
                    size.save()
                else:
                    size = size[0]
            product_size = ProductSize.objects.filter(size=size).filter(product=product)
            count = 0
            price = 0
            sale = 0
            if v[16] != "":
                count = v[16]
            if v[17] != "":
                price = v[17]
            try:
                if v[19] != "" and v[19] != 0:
                    sale = int(v[19])
            except:
                print('except')
            print(sale)
            if product_size.count() == 0:
                if (sale == 0):
                    product_size = ProductSize(product=product, size=size, price=price, count=count)
                else:
                    new_price = price - (price * sale / 100)
                    print(new_price)
                    product_size = ProductSize(product=product, size=size, old_price=price, count=count,
                                               sale=sale, price=new_price)
                product_size.save()
            else:
                if (sale == 0):
                    product_size = product_size[0]
                    product_size.price = price
                    product_size.count = count
                    product_size.sale = 0
                    product_size.old_price = 0
                else:
                    new_price = price - (price * sale / 100)
                    product_size = product_size[0]
                    product_size.price = new_price
                    product_size.count = count
                    product_size.sale = sale
                    product_size.old_price = price
                product_size.save()
            print(product)
    return HttpResponse(json.dumps(True))


def Product_image_save(request):
    print('Save_image_file')
    if request.method == 'POST':
        doc = request.FILES
        if (doc):
            for d in doc.getlist('image-file'):
                name = d.name.split('.')[0]
                product = Product.objects.filter(id=name)
                print(product)
                if product.count() > 0:
                    product = Product.objects.get(id=name)
                    product.main_photo = d
                    product.save()
    return HttpResponseRedirect("/admin")


# def News(request):
#     number, email = func_contact()
#     return render(request, 'Main/../templates/News/News.html', locals())


# def News_details(request):
#     number, email = func_contact()
#     return render(request, 'Main/../templates/News/News_details.html', locals())

# def Search_results(request):
#     dic = global_function(request)
#     return render(request, 'Main/Search_results.html', locals())


def Log_in(request):
    dic = global_function(request)
    if get_user_id(request) or request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Main'))
    else:
        return render(request, 'Main/Log_in.html', locals())


def Registration(request):
    dic = global_function(request)
    if get_user_id(request) or request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Main'))
    else:
        return render(request, 'Main/Registration.html', locals())


def check_login(request):
    try:
        email = request.GET.get('email')
        password = request.GET.get('password')
        if len(password) == 0 or len(email) == 0:
            return HttpResponse(json.dumps('Заполните поля!'))

        try:
            check_email = validate_email(email)
        except:
            return HttpResponse(json.dumps('Поля заполнены неверно!'))

        user = authenticate(username=email, password=password)

        if user is None:
            return HttpResponse(json.dumps('Логин или пароль введены неверно!'))
        else:
            # ses = request.session.get(settings.CART_SESSION_ID)
            login(request, user)
            request.session['username'] = AuthUser.objects.get(id=user.id).username
            # request.session[settings.CART_SESSION_ID] = ses
            request.session.modified = True
            return HttpResponse(json.dumps(True))
    except:
        return HttpResponse(json.dumps('Ошибка, попробуйте позже!'))


@transaction.atomic
def check_register(request):
    try:
        name = request.GET.get('name')
        surename = request.GET.get('surename')
        patronymic = request.GET.get('patronymic')
        phone = request.GET.get('phone')
        email = request.GET.get('email')
        adress = request.GET.get('adress')
        pass1 = request.GET.get('pass1')
        pass2 = request.GET.get('pass2')
        pass3 = pass1

        if AuthUser.objects.filter(email=email).exists():
            return HttpResponse(json.dumps('Аккаунт с такой почтой уже существует!'))

        try:
            check_email = validate_email(email)
        except:
            # check_email = False
            return HttpResponse(json.dumps('Email введён неверно!'))

        if len(name) == 0 or len(surename) == 0 or len(patronymic) == 0 or len(phone) == 0:
            return HttpResponse(json.dumps('Поля заполнены некоректно!'))

        # pass1=hashers.make_password(pass1)
        pass1 = hashlib.md5(pass1.encode('utf-8')).hexdigest()
        pass2 = hashlib.md5(pass2.encode('utf-8')).hexdigest()
        # print(pass1)
        # print(pass2)
        if pass1 != pass2:
            return HttpResponse(json.dumps('Пароли не совпадают!'))

        pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$')
        check_pass = bool(pattern_password.match(pass3))
        # print(check_pass)
        if not check_pass:
            return HttpResponse(json.dumps(
                'Пароль должен быть не менее 8 символов, содержать только латинские буквы, и как минимум одну заглавную букву и цифру!'))

        with transaction.atomic():
            # print(user.email)
            # print(user.password)
            email = str(email)
            password = str(pass3)

            user = User.objects.create_user(email, email, password)
            # user2.save()
            # print(user2)
            # print(type(user2))
            user1 = AuthUser.objects.get(username=user)
            user1.first_name = name
            user1.last_name = surename
            user1.save()

            # print(user2.id)
            us = Users(user_id=user1.id, patronymic=patronymic, phone=phone, city=adress, house='', street='', flat='')
            us.save()
            return HttpResponse(json.dumps(True))
    except:
        return HttpResponse(json.dumps('Ошибка, попробуйте позже!'))


def error404(request, exception):
    dic = global_function(request)
    return render(request, '404.html', locals())
