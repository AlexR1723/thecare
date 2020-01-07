from django.shortcuts import render
from .models import *

# Create your views here.

def Deliveries(request):
    list = Delivery.objects.all()
    return render(request, 'Delivery/Delivery.html', locals())