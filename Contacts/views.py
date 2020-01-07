from django.shortcuts import render

# Create your views here.

def Contacts(request):
    return render(request, 'Contacts/Contacts.html', locals())