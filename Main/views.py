from django.shortcuts import render

# Create your views here.
def Main(request):
    return render(request, 'Main/Main.html', locals())

def Dev(request):
    return render(request, 'Main/Dev.html', locals())

def Delivery(request):
    return render(request, 'Main/Delivery.html', locals())

def Payment(request):
    return render(request, 'Main/Payment.html', locals())