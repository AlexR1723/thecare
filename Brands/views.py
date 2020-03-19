from django.shortcuts import render
from .models import *
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

def Brands(request):
    dic = global_function(request)

    items=Brands_model.objects.all().order_by('name')
    return render(request, 'Brands/Brands.html', locals())