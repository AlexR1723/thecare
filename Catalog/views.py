from django.shortcuts import render

# Create your views here.


def Items_catalog(request):
    return render(request, 'Catalog/Items_catalog.html', locals())

def Face(request):
    return render(request, 'Catalog/Items_catalog.html', locals())