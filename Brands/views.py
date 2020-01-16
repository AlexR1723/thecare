from django.shortcuts import render
from .models import *

def func_contact():
    number = Contact.objects.filter(is_main=True, contact_id=2)[0].text
    email=Contact.objects.filter(is_main=True,contact_id=4)[0].text
    return number, email

def Brands(request):
    number, email = func_contact()

    items=Brands_model.objects.all().order_by('name')
    return render(request, 'Brands/Brands.html', locals())