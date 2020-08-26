from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.validators import validate_email
import json, requests, geocoder
from pysendpulse.pysendpulse import PySendPulse
from django.conf import settings


def Contacts(request):
    list = Contact.objects.all()
    numbers = list.filter(contact_id=2)
    emails = list.filter(contact_id=4)
    grafic = list.filter(contact_id=3)
    adress = list.filter(contact_id=1)
    map = list.filter(contact_id=5)[0].text
    return render(request, 'Contacts/Contacts.html', locals())


def send_feedback(request):
    name = str(request.GET.get('name')).strip()
    email = str(request.GET.get('email')).strip()
    subj = str(request.GET.get('subject')).strip()
    text = str(request.GET.get('text')).strip()
    try:
        check_email = validate_email(email)
    except:
        check_email = False
    if not name or len(name) < 2 or not email or not text or check_email == False or len(name) > 100 or len(
            email) > 200 or len(subj) > 300:
        return HttpResponse(json.dumps(False))
    else:
        # user = request.session.get('username', False)
        # if user:
        #     fb = Feedback(user_id=AuthUser.objects.get(username=user).id, name=name, email=email, subject=subj,
        #                   text=text)
        # else:
        #     fb = Feedback(name=name, email=email, subject=subj, text=text)
        # fb.save()
        print('send mail')
        SPApiProxy = PySendPulse(settings.EMAIL_REST_API_ID, settings.EMAIL_REST_API_SECRET, 'memcached')
        email = {
            'subject': 'Обратная связь',
            'html': '<h1>Hello, Anastason!</h1><p>This message is only sent to very pretty girls!</p>',
            'text': '',
            'from': {'name': 'The Care', 'email': 'mail@thecare.ru'},
            'to': [
                {'name': 'Direct', 'email': 'thecare.shop@yandex.ru'}
            ]
        }
        # sending = SPApiProxy.smtp_send_mail(email)
        # print(sending)


    return HttpResponse(json.dumps(True))
