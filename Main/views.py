from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import xlrd, xlwt, json, re, hashlib
from django.contrib.auth import authenticate, login, logout, hashers
from django.core.validators import validate_email
from django.db import transaction
from django.contrib.auth.models import User

import os


def func_contact():
    number = Contact.objects.filter(is_main=True, contact_id=2)[0].text
    email = Contact.objects.filter(is_main=True, contact_id=4)[0].text
    return number, email


def Main(request):
    number, email = func_contact()
    slide_first = Slider.objects.all()[0]
    slide = Slider.objects.all()[1:]
    main_block = MainBlock.objects.all()
    face_count = Product.objects.order_by('-id').filter(category__name='Для лица').count()
    if face_count < 10:
        face = Product.objects.order_by('-id').filter(category__name='Для лица')
    else:
        face = Product.objects.order_by('-id').filter(category__name='Для лица')[0:10]
    print(face)
    hair_count = Product.objects.order_by('-id').filter(category__name='Для волос').count()
    if hair_count < 10:
        hair = Product.objects.order_by('-id').filter(category__name='Для волос')
    else:
        hair = Product.objects.order_by('-id').filter(category__name='Для волос')[0:10]
    print(hair)
    body_count = Product.objects.order_by('-id').filter(category__name='Для тела').count()
    if body_count < 10:
        body = Product.objects.order_by('-id').filter(category__name='Для тела')
    else:
        body = Product.objects.order_by('-id').filter(category__name='Для тела')[0:10]
    print(body)
    return render(request, 'Main/Main.html', locals())


def Dev(request):
    number, email = func_contact()
    return render(request, 'Main/Dev.html', locals())


def Save_excel_file(request):
    print('Save_excel_file')
    if request.method == 'POST':
        doc = request.FILES
        if (doc):
            print(doc['excel-file'])
            file = Files(file=doc['excel-file'])
            file.save()
            print(file.file.path)
            rb = xlrd.open_workbook(file.file.path)
            sheet = rb.sheet_by_index(0)
            vals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]
            for v in vals:
                if v[1] != "" and v[1] != "Привязка к позиции":
                    categ = CategoryType.objects.filter(name=v[8])
                    print(categ)
                    res = ResourceType.objects.filter(name=v[9])
                    print(res)
                    brand = Brands_model.objects.filter(name=v[2])
                    if brand.count() == 0:
                        brand = Brands_model(name=v[2])
                        brand.save()
                    else:
                        brand = Brands_model.objects.get(name=v[2])
                    print(brand)
                    print(v[12])
                    size = Size.objects.filter(name=v[12])
                    print(size)
                    product = Product.objects.filter(title=v[3])
                    if categ.count() > 0 and res.count() > 0 and size.count() > 0:
                        if product.count() == 0:
                            print(1)
                            product = Product(title=v[3], shot_description=v[4], description=v[5], note=v[6],
                                              components=v[7],
                                              category=categ[0], resource=res[0], brand=brand)
                            # product = Product(title=v[3], shot_description=v[4], description=v[5], note=v[6],
                            #                   components=v[7],
                            #                   category=categ, resource=res, artikul=v[13], price=v[15], brand=brand[0])
                            product.save()
                            needs = v[10]
                            list_need = needs.split(', ')
                            if list_need.count == 0:
                                need = NeedType.objects.filter(name=needs)
                                if need.count() > 0:
                                    product_need = ProductNeed(product=product, need=need[0])
                                    product_need.save()
                            else:
                                for n in list_need:
                                    need = NeedType.objects.filter(name=n)
                                    if need.count() > 0:
                                        product_need = ProductNeed(product=product, need=need[0])
                                        product_need.save()
                            print(2)
                        else:
                            product = product[0]
                        product_size = ProductSize.objects.filter(size=size[0]).filter(product=product)
                        print(product_size)
                        if product_size.count == 0:
                            product_size = ProductSize(product=product, size=size[0])
                            product_size.save()
                        print(product)
    return HttpResponseRedirect("/admin")


# def News(request):
#     number, email = func_contact()
#     return render(request, 'Main/../templates/News/News.html', locals())


# def News_details(request):
#     number, email = func_contact()
#     return render(request, 'Main/../templates/News/News_details.html', locals())

def Search_results(request):
    number, email = func_contact()
    return render(request, 'Main/Search_results.html', locals())


def Cart(request):
    number, email = func_contact()
    return render(request, 'Main/Cart.html', locals())


def Log_in(request):
    number, email = func_contact()
    return render(request, 'Main/Log_in.html', locals())


def Registration(request):
    number, email = func_contact()
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
            login(request, user)
            request.session['username'] = AuthUser.objects.get(id=user.id).username
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
        # print(pass1)
        # print(pass2)
        pass3 = pass1

        if AuthUser.objects.filter(email=email).exists():
            return HttpResponse(json.dumps('Аккаунт с такой почтой уже существует!'))

        try:
            check_email = validate_email(email)
        except:
            check_email = False
            return HttpResponse(json.dumps('Email введён неверно!'))

        if len(name) == 0 or len(surename) == 0 or len(patronymic) == 0 or len(phone) == 0:
            return HttpResponse(json.dumps('Поля заполнены некоректно!'))

        # pass1=hashers.make_password(pass1)
        pass1 = hashlib.md5(pass1.encode('utf-8')).hexdigest()
        pass2 = hashlib.md5(pass2.encode('utf-8')).hexdigest()
        # print(pass1)
        print(pass2)
        if pass1 != pass2:
            return HttpResponse(json.dumps('Пароли не совпадают!'))

        pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$')
        check_pass = bool(pattern_password.match(pass3))
        # print(check_pass)
        if not check_pass:
            return HttpResponse(json.dumps(
                'Пароль должен быть не менее 8 символов, содержать только латинские буквы, как минимум одну заглавную букву и цифру!'))

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
            us = Users(user_id=user1.id, patronymic=patronymic, phone=phone, adress=adress)
            us.save()
            return HttpResponse(json.dumps(True))
    except:
        return HttpResponse(json.dumps('Ошибка, попробуйте позже!'))
