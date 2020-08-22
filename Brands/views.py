from django.shortcuts import render
from .models import *
from django.conf import settings


def Brands(request):
    # dic = global_function(request)

    items = Brands_model.objects.order_by('name')
    letter = []
    l=[]
    for i in items:
        if i.name[0] not in l:
            l.append(i.name[0])
    for i in l:
        t = []
        t.append(i)
        brand = Brands_model.objects.filter(name__istartswith=i)
        t.append(brand)
        letter.append(t)
    # print(letter)
    return render(request, 'Brands/Brands.html', locals())
