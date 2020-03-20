from django.shortcuts import render
from .models import *
from django.conf import settings
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

def Brands(request):
    dic = global_function(request)

    items=Brands_model.objects.all().order_by('name')
    letter=[]
    for i in items:
        if not i.name in letter:
            t=[]
            t.append(i.name[0])
            brand=Brands_model.objects.filter(name__istartswith=i.name[0])
            t.append(brand)
            letter.append(t)
    print(letter)
    return render(request, 'Brands/Brands.html', locals())