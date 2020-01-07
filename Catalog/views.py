from django.shortcuts import render
from .models import *
# Create your views here.


def Items_catalog(request):
    return render(request, 'Catalog/Items_catalog.html', locals())

def Face(request):
    head='Средства для лица'
    product=Product.objects.all()
    resource=ResourceType.objects.filter(category__name='Для лица')
    need=NeedType.objects.filter(category__name='Для лица')
    return render(request, 'Catalog/Items_catalog.html', locals())