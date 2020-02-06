from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import xlrd, xlwt

import os

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


def Save_excel_file(request):
    print('Save_excel_file')
    if request.method == 'POST':
        doc = request.FILES
        if (doc):
            print(doc['excel-file'])
            file=Files(file=doc['excel-file'])
            file.save()
            print(file.file.path)
            rb = xlrd.open_workbook(file.file.path)
            sheet = rb.sheet_by_index(0)
            vals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]
            for v in vals:
                if v[2] != "" and v[2] != "Бренд (производитель)":
                    categ=CategoryType.objects.get(name=v[8])
                    print(categ)
                    res=ResourceType.objects.get(name=v[9])
                    print(res)
                    brand=Brands_model.objects.get(name=v[2])
                    print(brand)
                    product=Product(title=v[3], shot_description=v[4],description=v[5],note=v[6],components=v[7],
                                    category=categ,resource=res, size=v[12], artikul=v[13],price=v[15], brand=brand)
                    product.save()
                    print(product)
                    needs=v[10]
                    list_need=needs.split(', ')
                    for n in list_need:
                        need=NeedType.objects.get(name=n)
                        product_need=ProductNeed(product=product,need=need)
                        product_need.save()
    return HttpResponseRedirect("/admin")

# def News(request):
#     number, email = func_contact()
#     return render(request, 'Main/../templates/News/News.html', locals())



# def News_details(request):
#     number, email = func_contact()
#     return render(request, 'Main/../templates/News/News_details.html', locals())

def Search_results(request):
    number, email = func_contact()
    return render(request, 'Main/Search_results.html', locals())

def Cart(request):
    number, email = func_contact()
    return render(request, 'Main/Cart.html', locals())



