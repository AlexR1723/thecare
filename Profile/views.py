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
from django.contrib.auth.decorators import login_required

from django.conf import settings


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


# Create your views here.
@login_required()
def Orders_history(request):
    dic = global_function(request)
    print(get_user_id(request))
    return render(request, 'Main/Orders_history.html', locals())


@login_required()
def Delivery_address(request):
    dic = global_function(request)
    return render(request, 'Main/Delivery_address.html', locals())


@login_required()
def Contact_details(request):
    dic = global_function(request)

    id=get_user_id(request)
    user=AuthUser.objects.get(id=id)
    users=Users.objects.get(user_id=id)
    return render(request, 'Main/Contact_details.html', locals())


@login_required()
def Logout(request):
    # dic = global_function(request)
    logout(request)
    return HttpResponseRedirect("/")


def change_contact_details(request):
    user = get_user_id(request)
    if user:
        name = str(request.GET.get('name')).strip()
        surname = str(request.GET.get('surname')).strip()
        patron = str(request.GET.get('patron')).strip()
        email = request.GET.get('email')
        phone = str(request.GET.get('phone')).strip()
        address = request.GET.get('address')
        pass1 = request.GET.get('pass1')
        pass2 = request.GET.get('pass2')
        pass3 = request.GET.get('pass3')


        if AuthUser.objects.filter(email=email).exists() and AuthUser.objects.get(id=user).email!=email:
            return HttpResponse(json.dumps('Аккаунт с такой почтой уже существует!'))
        if len(name) == 0 or len(surname) == 0 or len(patron) == 0 or len(phone)==0:
            return HttpResponse(json.dumps('Заполните все необходимые поля!'))
        try:
            check_email = validate_email(email)
        except:
            return HttpResponse(json.dumps('Неверно заполнен E-mail!'))

        user1=AuthUser.objects.get(id=user)
        user1.first_name=name
        user1.last_name=name
        user1.email=email
        user1.username=email
        user1.save()

        user2=Users.objects.get(user_id=user)
        user2.patronymic=patron
        user2.phone=phone
        user2.address=address
        user2.save()

        if pass1 or pass2 or pass3:
            if pass1 and pass2 and pass3:
                us = AuthUser.objects.get(id=user)
                if User.check_password(us, pass1):
                    if pass2 == pass3:
                        if pass1 == pass2:
                            return HttpResponse(json.dumps('Новый пароль не должен совпадать со старым!'))
                        pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$')
                        check_pass = bool(pattern_password.match(pass2))
                        if check_pass:
                            new_pass = hashers.make_password(pass2)
                            us.password = new_pass
                            us.save()
                            # return HttpResponse(json.dumps('Пароль успешно изменён!'))
                        else:
                            return HttpResponse(json.dumps(
                                'Пароль должен быть не менее 8 символов, содержать только латинские буквы, и как минимум одну заглавную букву и цифру!'))
                    else:
                        return HttpResponse(json.dumps('Пароли не совпадают!'))
                else:
                    return HttpResponse(json.dumps('Старый пароль введен неверно!'))
            else:
                return HttpResponse(json.dumps('Заполните все поля для изменения пароля!'))
        return HttpResponse(json.dumps('Данные успешно изменены!'))
    else:
        return HttpResponse(json.dumps(False))
