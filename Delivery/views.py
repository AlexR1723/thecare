from django.shortcuts import render
from .models import *

def func_contact():
    number = Contact.objects.filter(is_main=True, contact_id=2)[0].text
    email=Contact.objects.filter(is_main=True,contact_id=4)[0].text
    return number, email


def Deliveries(request):
    number, email = func_contact()

    list = Delivery.objects.all()
    return render(request, 'Delivery/Delivery.html', locals())