from django.shortcuts import render
from .models import *

def func_contact():
    number = Contact.objects.filter(is_main=True, contact_id=2)[0].text
    email=Contact.objects.filter(is_main=True,contact_id=4)[0].text
    return number, email


def Items_catalog(request):
    number, email = func_contact()

    return render(request, 'Catalog/Items_catalog.html', locals())

def Face(request):
    number, email = func_contact()

    head='Средства для лица'
    product=Product.objects.all()
    resource=ResourceType.objects.filter(category__name='Для лица')
    need=NeedType.objects.filter(category__name='Для лица')
    return render(request, 'Catalog/Items_catalog.html', locals())

def Item_card(request):
    number, email = func_contact()
    return render(request, 'Catalog/Item_card.html', locals())