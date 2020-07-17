from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.validators import validate_email
import json,requests,geocoder

from django.conf import settings

# def global_function(request):
#     number = Contact.objects.filter(is_main=True, contact_id=2)[0].text
#     email = Contact.objects.filter(is_main=True, contact_id=4)[0].text
#
#     ses = request.session.get(settings.CART_SESSION_ID)
#     ids = []
#     for i in ses.keys():
#         ids.append(int(i))
#     prods = ProductSize.objects.filter(id__in=ids)
#     for i in ids:
#         prod = prods.filter(id=i)[0]
#         count = ses[str(i)]['count']
#         ses[str(i)]['total'] = prod.price * count
#
#     basket = 0
#     ses = request.session.get(settings.CART_SESSION_ID)
#     if ses and ses is not None:
#         for i in ses.values():
#             basket += int(i['total'])
#
#     is_auth = request.user.is_authenticated
#     if is_auth:
#         is_auth = request.session.get('username', False)
#
#     user_name = ''
#     if is_auth:
#         user_name = AuthUser.objects.get(username=is_auth).first_name
#
#     result_dict = {
#         'number': number,
#         'email': email,
#         'basket': basket,
#         'is_auth': is_auth,
#         'user_name': user_name
#     }
#     return result_dict


def Contacts(request):
    # dic = global_function(request)
    # dic=request
    list = Contact.objects.all()
    numbers=list.filter(contact_id=2)
    emails=list.filter(contact_id=4)
    grafic=list.filter(contact_id=3)
    adress=list.filter(contact_id=1)
    map=list.filter(contact_id=5)[0].text

    return render(request, 'Contacts/Contacts.html', locals())

def send_feedback(request):
    name=str(request.GET.get('name')).strip()
    email=str(request.GET.get('email')).strip()
    subj=str(request.GET.get('subject')).strip()
    text=str(request.GET.get('text')).strip()
    try:
        check_email = validate_email(email)
    except:
        check_email=False
    if not name or len(name)<2 or not email or not text or check_email==False or len(name)>100 or len(email)>200 or len(subj)>300:
        return HttpResponse(json.dumps(False))
    else:
        user = request.session.get('username', False)
        if user:
            fb=Feedback(user_id=AuthUser.objects.get(username=user).id,name=name,email=email,subject=subj,text=text)
        else:
            fb = Feedback(name=name, email=email, subject=subj, text=text)
        # fb.save()

    # import
    # url = 'https://maps.googleapis.com/maps/api/geocode/json'
    # params = {'sensor': 'false', 'address': 'Моксва'}
    # r = requests.get(url, params=params)
    # print(r)
    # results = r.json()['results']
    # # results = r
    # print(results)
    # location = results[0]['geometry']['location']
    # print(location)
    # # location['lat'], location['lng']
    # print(location['lat'])
    # print(location['lng'])

    # g = geocoder.google('Moscow Lenina')
    # print(g.latlng)

    return HttpResponse(json.dumps(True))