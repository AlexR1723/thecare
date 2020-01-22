"""work URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    url(r'^face/$', views.Face, name="Face"),
    url(r'^for_men/$', views.For_men, name="For_men"),
    # url(r'^for_men/$', views.For_men_s, name="For_men_s"),
    # url(r'^for_men/(?P<text>)/$', views.For_men_s, name="For_men_s"),
    path('for_men/<str:text>/', views.For_men_s),
    # url(r'^for_men/(?P<text>[А-Яа-я\s0-9-()/a-z,:]+)/$', views.For_men_s, name="For_men_s"),
    url(r'^items_catalog/$', views.Items_catalog, name="Items_catalog"),
    # url(r'^item_card/$', views.Item_card, name="Item_card"),
    path('<slug:slug>', views.Item_card, name='Item_card'),
]
