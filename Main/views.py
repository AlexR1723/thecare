from django.shortcuts import render
from .models import *
# Create your views here.
def Main(request):
    return render(request, 'Main/Main.html', locals())

def Dev(request):
    # list = A
    return render(request, 'Main/Dev.html', locals())

