from django.shortcuts import render

# Create your views here.

def Delivery(request):
    return render(request, 'Delivery/Delivery.html', locals())