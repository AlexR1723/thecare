from django.shortcuts import render
from .models import *

def func_contact():
    number = Contact.objects.filter(is_main=True, contact_id=2)[0].text
    email=Contact.objects.filter(is_main=True,contact_id=4)[0].text
    return number, email


def Main(request):
    number, email = func_contact()
    return render(request, 'Main/Main.html', locals())

def Dev(request):
    number, email = func_contact()
    return render(request, 'Main/Dev.html', locals())

def Brands(request):
    number, email = func_contact()
    return render(request, 'Main/Brands.html', locals())

def News(request):
    number, email = func_contact()
    return render(request, 'Main/News.html', locals())



