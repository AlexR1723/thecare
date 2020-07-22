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
import dropbox
import os
from django.conf import settings
from django.views.decorators.cache import cache_page

list = []
list_count = 0


# def global_function(request):
#     number = Contact.objects.filter(is_main=True, contact_id=2)[0].text
#     email = Contact.objects.filter(is_main=True, contact_id=4)[0].text
#
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

@cache_page(600, cache='default', key_prefix='')
def Main(request):
    slide_first = Slider.objects.all()[0]
    slide = Slider.objects.all()[1:]
    main_block = MainBlock.objects.all()
    face = Product.objects.filter(is_top=True).filter(category__name='Для лица').order_by('-id')
    hair = Product.objects.filter(is_top=True).filter(category__name='Для волос').order_by('-id')
    body = Product.objects.filter(is_top=True).filter(category__name='Для тела').order_by('-id')
    # k = 0
    # if k == 0:

    # else:
    return render(request, 'Main/Main.html', locals())


def Dev(request):
    raise Http404("aasdsd")
    # return HttpResponseNotFound('<h1>Page not found</h1>')
    # return HttpResponse(status=404)


def Save_excel_file(request):
    print('Save_excel_file')
    if request.method == 'POST':
        settings.TOP=str(request.POST.get('top'))
        print(settings.TOP)
        doc = request.FILES
        if (doc):
            settings.PROD_LIST.clear()
            settings.DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
            print(doc['excel-file'])
            file = Files(file=doc['excel-file'])
            file.save()
            # print(file.file.path)
            rb = xlrd.open_workbook(file.file.path)

            sheet = rb.sheet_by_index(0)
            vals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]
            for v in vals:
                try:
                    settings.PROD_LIST.append(v)
                except:
                    print('ex1')
            settings.DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
            list_count = len(settings.PROD_LIST)
            print(len(settings.PROD_LIST))
    return HttpResponseRedirect("/admin")


def get_product_count(request):
    return HttpResponse(json.dumps(len(settings.PROD_LIST)))


def get_product_list(request):
    return HttpResponse(json.dumps(settings.PROD_LIST))

def get_top(request):
    return HttpResponse(json.dumps(settings.TOP))

# def get_brands_list(request):
#     brands=Brands_model.objects.order_by('name')
#     brands_list=[]
#     for i in brands:
#         brands_list.append([i.id,i.name])
#     return HttpResponse(json.dumps(brands_list))
#
#
# def get_sale_brand(request):
#     brand=int(request.GET.get('brand'))
#     product=ProductSize.objects.filter(product__brand__id=brand).order_by('-sale')
#     print(product[0].sale)
#     # brands=Brands_model.objects.order_by('name')
#     # brands_list=[]
#     # for i in brands:
#     #     brands_list.append([i.id,i.name])
#     return HttpResponse(product[0].sale)


def save_product(request):
    # добавить выборку каждой переменной
    print('save_product')
    try:
        i = int(request.GET.get('i'))
        all = int(request.GET.get('all'))
        # print(i+1)
        if (i + 1) >= all:
            # print('clear')
            settings.PROD_LIST.clear()
        # print(i)
        file = Files.objects.last()
        rb = xlrd.open_workbook(file.file.path)

        sheet = rb.sheet_by_index(0)
        v = sheet.row_values(i)
        print(v)
        if v is not None:
            # print(v)
            # категория (для волос, для тела и тд)
            categ = CategoryType.objects.filter(name=v[8])
            # наименование средства
            res = ResourceType.objects.filter(category=categ[0]).filter(name=v[9])
            if res.count() == 0:
                res = ResourceType(category=categ[0], name=v[9])
                res.save()
            else:
                res = res[0]
            if categ.count() > 0:
                brand = Brands_model.objects.filter(name__iexact=v[2])
                if brand.count() == 0:
                    brand = Brands_model(name=v[2])
                    brand.save()
                else:
                    brand = brand[0]
                # выбираем товар, где картинка текст
                print(v[3])
                print(v[2])
                print(v[4])
                product_str = Product_str.objects.filter(title__iexact=v[4]).filter(brand__name__iexact=v[2]).filter(
                    shot_description__iexact=v[3])
                # такого товара нет - добавили
                if product_str.count() == 0:
                    print('if')
                    product_str = Product_str(title=v[4], shot_description=v[3], description=v[5], note=v[6],
                                              components=v[7],
                                              category=categ[0], resource=res, brand=brand, artikul=v[14],
                                              artik_brand=v[15], main_photo="uploads/product/" + v[11])
                    product_str.save()
                    # if len(v) > 20:
                    #     if str(v(20)).find('+') != -1:
                    #         product_str.hit_for_brand = True
                    #         product_str.save()
                # такой товар есть - обновили
                else:
                    print('else')
                    product_str = product_str[0]
                    product_str.description = v[5]
                    product_str.note = v[6]
                    product_str.components = v[7]
                    product_str.category = categ[0]
                    product_str.resource = res
                    product_str.brand = brand
                    product_str.artikul = v[14]
                    product_str.artik_brand = v[15]
                    product_str.main_photo = "uploads/product/" + v[11]
                    product_str.save()
                    # if len(v) > 20:
                    #     if str(v(20)).find('+') != -1:
                    #         product_str.hit_for_brand = True
                    #         product_str.save()
                # выбираем товар
                product = Product.objects.get(id=product_str.id)
                print(product)

                # потребности товара
                # удаляем старые потребности
                product_need = ProductNeed.objects.filter(product=product)
                product_need.delete()
                # выбираем новые потребности
                needs = v[10]
                list_need = needs.split(', ')
                if len(list_need) == 1:
                    need = NeedType.objects.filter(name__iexact=needs).filter(category=categ[0])
                    if need.count() == 0:
                        need = NeedType(name=needs, category=categ[0])
                        need.save()
                    else:
                        need = need[0]
                    product_need = ProductNeed.objects.filter(product=product).filter(need=need)
                    if product_need.count() == 0:
                        product_need = ProductNeed(product=product, need=need)
                        product_need.save()
                else:
                    for n in list_need:
                        need = NeedType.objects.filter(name__iexact=n).filter(category=categ[0])
                        if need.count() == 0:
                            need = NeedType(name=n, category=categ[0])
                            need.save()
                        else:
                            need = need[0]
                        product_need = ProductNeed.objects.filter(need=need).filter(product=product)
                        if product_need.count() == 0:
                            product_need = ProductNeed(product=product, need=need)
                            product_need.save()

                # объем
                # удаляем старые объемы
                # product_size = ProductSize.objects.filter(product=product)
                # product_size.delete()
                # выбираем новые объемы
                if v[12] == "":
                    size_name = 0
                else:
                    size_name = v[12]
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
                print(size)
                count = 0
                price = 0
                sale = 0
                if v[16] and v[16] != "":
                    count = int(v[16])
                if v[17] and v[17] != "":
                    price = int(v[17])
                if v[19] and v[19] != "":
                    sale = int(v[19])
                if sale == 0:
                    print('if_size')
                    product_size = ProductSize.objects.filter(product=product).filter(size=size)
                    if product_size.count() == 0:
                        product_size = ProductSize(product=product, size=size, price=price, count=count)
                        product_size.save()
                    else:
                        product_size.price = price
                        product_size.count = count
                        product_size.save()
                    print(product_size)
                else:
                    print('else_size')
                    new_price = price - (price * sale / 100)
                    product_size = ProductSize.objects.filter(product=product).filter(size=size)
                    if product_size.count() == 0:
                        product_size = ProductSize(product=product, size=size, old_price=price, count=count, sale=sale,
                                                   price=new_price)
                        product_size.save()
                    else:
                        product_size.old_price = price
                        product_size.count = count
                        product_size.sale = sale
                        product_size.price = new_price
                        product_size.save()
                    print(product_size)

                # оттенки
                # удаляем старые оттенки
                product_tone = ProductTone.objects.filter(product=product)
                product_tone.delete()
                # выбираем новые оттенки
                if v[13] != "" and v[13] != " ":
                    tones = v[13]
                    list_tone = tones.split('; ')
                    if list_tone != "" and len(list_tone) != 0:
                        for t in list_tone:
                            product_tone = ProductTone(product=product, name=t)
                            product_tone.save()

            # if i+1 == len(settings.PROD_LIST):

            return HttpResponse(json.dumps(True))
        else:
            return HttpResponse(json.dumps('not save'))
    except:
        return HttpResponse(json.dumps(False))

def del_product_top(request):
    products=Product.objects.filter(is_top=True)
    for p in products:
        p.is_top=False
        p.save()
    return HttpResponse(json.dumps(True))

def top_product_save(request):
    # добавить выборку каждой переменной
    print('save_product_top')
    try:
        i = int(request.GET.get('i'))
        all = int(request.GET.get('all'))
        # print(i+1)
        if (i + 1) >= all:
            # print('clear')
            settings.PROD_LIST.clear()
        # print(i)
        file = Files.objects.last()
        rb = xlrd.open_workbook(file.file.path)

        sheet = rb.sheet_by_index(0)
        v = sheet.row_values(i)
        print(len(v))
        print(v)
        if v[2] != None and v[2] != '':
            if v is not None:
                # print(v)
                # категория (для волос, для тела и тд)
                categ = CategoryType.objects.filter(name=v[8])
                # наименование средства
                res = ResourceType.objects.filter(category=categ[0]).filter(name=v[9])
                if res.count() == 0:
                    res = ResourceType(category=categ[0], name=v[9])
                    res.save()
                else:
                    res = res[0]
                if categ.count() > 0:
                    brand = Brands_model.objects.filter(name__iexact=v[2])
                    if brand.count() == 0:
                        brand = Brands_model(name=v[2])
                        brand.save()
                    else:
                        brand = brand[0]
                    # выбираем товар, где картинка текст
                    print(v[3])
                    print(v[2])
                    print(v[4])
                    product_str = Product_str.objects.filter(title__iexact=v[4]).filter(brand__name__iexact=v[2]).filter(
                        shot_description__iexact=v[3])
                    # такого товара нет - добавили
                    if product_str.count() == 0:
                        print('if')
                        product_str = Product_str(title=v[4], shot_description=v[3], description=v[5], note=v[6],
                                                  components=v[7],
                                                  category=categ[0], resource=res, brand=brand, artikul=v[14],
                                                  artik_brand=v[15], main_photo="uploads/product/" + v[11], is_top = 1)
                        product_str.save()
                        # if len(v) > 20:
                        #     if str(v(20)).find('+') != -1:
                        #         product_str.hit_for_brand=True
                        #         product_str.save()
                    # такой товар есть - обновили
                    else:
                        print('else')
                        product_str = product_str[0]
                        product_str.description = v[5]
                        product_str.note = v[6]
                        product_str.components = v[7]
                        product_str.category = categ[0]
                        product_str.resource = res
                        product_str.brand = brand
                        product_str.artikul = v[14]
                        product_str.artik_brand = v[15]
                        product_str.main_photo = "uploads/product/" + v[11]
                        product_str.is_top = 1
                        product_str.save()
                        print(product_str.is_top)
                        # if len(v)>20:
                        #     if str(v(20)).find('+') != -1:
                        #         product_str.hit_for_brand=True
                        #         product_str.save()
                    # выбираем товар
                    product = Product.objects.get(id=product_str.id)
                    print(product)

                    # потребности товара
                    # удаляем старые потребности
                    product_need = ProductNeed.objects.filter(product=product)
                    product_need.delete()
                    # выбираем новые потребности
                    needs = v[10]
                    list_need = needs.split(', ')
                    if len(list_need) == 1:
                        need = NeedType.objects.filter(name__iexact=needs).filter(category=categ[0])
                        if need.count() == 0:
                            need = NeedType(name=needs, category=categ[0])
                            need.save()
                        else:
                            need = need[0]
                        product_need = ProductNeed.objects.filter(product=product).filter(need=need)
                        if product_need.count() == 0:
                            product_need = ProductNeed(product=product, need=need)
                            product_need.save()
                    else:
                        for n in list_need:
                            need = NeedType.objects.filter(name__iexact=n).filter(category=categ[0])
                            if need.count() == 0:
                                need = NeedType(name=n, category=categ[0])
                                need.save()
                            else:
                                need = need[0]
                            product_need = ProductNeed.objects.filter(need=need).filter(product=product)
                            if product_need.count() == 0:
                                product_need = ProductNeed(product=product, need=need)
                                product_need.save()

                    # объем
                    # удаляем старые объемы
                    # product_size = ProductSize.objects.filter(product=product)
                    # product_size.delete()
                    # выбираем новые объемы
                    if v[12] == "":
                        size_name = 0
                    else:
                        size_name = v[12]
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
                    print(size)
                    count = 0
                    price = 0
                    sale = 0
                    if v[16] and v[16] != "":
                        count = int(v[16])
                    if v[17] and v[17] != "":
                        price = int(v[17])
                    if v[19] and v[19] != "":
                        sale = int(v[19])
                    if sale == 0:
                        print('if_size')
                        product_size=ProductSize.objects.filter(product=product).filter(size=size)
                        if product_size.count() == 0:
                            product_size = ProductSize(product=product, size=size, price=price, count=count)
                            product_size.save()
                        else:
                            product_size.price=price
                            product_size.count=count
                            product_size.save()
                        print(product_size)
                    else:
                        print('else_size')
                        new_price = price - (price * sale / 100)
                        product_size = ProductSize.objects.filter(product=product).filter(size=size)
                        if product_size.count() == 0:
                            product_size = ProductSize(product=product, size=size, old_price=price, count=count, sale=sale,
                                                   price=new_price)
                            product_size.save()
                        else:
                            product_size.old_price = price
                            product_size.count = count
                            product_size.sale=sale
                            product_size.price=new_price
                            product_size.save()
                        print(product_size)

                    # оттенки
                    # удаляем старые оттенки
                    product_tone = ProductTone.objects.filter(product=product)
                    product_tone.delete()
                    # выбираем новые оттенки
                    if v[13] != "" and v[13] != " ":
                        tones = v[13]
                        list_tone = tones.split('; ')
                        if list_tone != "" and len(list_tone) != 0:
                            for t in list_tone:
                                product_tone = ProductTone(product=product, name=t)
                                product_tone.save()

                # if i+1 == len(settings.PROD_LIST):

                return HttpResponse(json.dumps(True))
            else:
                return HttpResponse(json.dumps('not save'))
        else:
            return HttpResponse(json.dumps(True))
    except:
        return HttpResponse(json.dumps(False))


def check_picture(request):
    # print(response)
    # f = open('list_images.txt', 'w')
    # f.truncate()
    data = []
    products = Product.objects.all()
    for i in products:
        data.append(str(i.main_photo))
    # data = f.read()
    # f.close()

    # data = data.split(';')
    lst = []
    for i in data:
        st = i.replace('uploads/product/', '')
        lst.append(st)

    lst_not = []
    dirs = []
    dbx = dropbox.Dropbox(settings.DROPBOX_OAUTH2_TOKEN)
    response = dbx.files_list_folder(path=settings.DROPBOX_ROOT_PATH + 'uploads/product')
    if response.has_more == True:
        m1 = response.entries
        cur = response.cursor
        for i in m1:
            if isinstance(i, dropbox.files.FileMetadata):
                dirs.append(i.name)
        m2 = dbx.files_list_folder_continue(cur)
        if m2.has_more == True:
            while m2.has_more == True:
                for i in m2.entries:
                    if isinstance(i, dropbox.files.FileMetadata):
                        dirs.append(i.name)
                cur = m2.cursor
                m2 = dbx.files_list_folder_continue(cur)
        else:
            cur = response.cursor
            m_final = dbx.files_list_folder_continue(cur)
            for i in m_final.entries:
                if isinstance(i, dropbox.files.FileMetadata):
                    dirs.append(i.name)
    print(len(dirs))
    print(len(lst))
    for i in lst:
        # print(i)
        if i not in dirs:
            # print(i)
            lst_not.append(i)
            # print(i + ' not in dirs')
    # print(lst_not)
    return HttpResponse(json.dumps(lst_not))


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
    # dic = global_function(request)
    if get_user_id(request) or request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Main'))
    else:
        return render(request, 'Main/Log_in.html', locals())


def Registration(request):
    # dic = global_function(request)
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


def handler404(request,exception):
    return render(request, '404.html', locals())


def success(request):
    return render(request, 'success.html', locals())



def robots_txt(request):
    return render(request, 'robots.txt', locals())

def sitemap_xml(request):
    return render(request, 'sitemap.xml', locals())