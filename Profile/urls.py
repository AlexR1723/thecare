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

urlpatterns = [
    url(r'^$', views.Orders_history, name="Orders_history"),
    url(r'^delivery_address/$', views.Delivery_address, name="Delivery_address"),
    url(r'^contact_details/$', views.Contact_details, name="Contact_details"),
    url(r'^logout/$', views.Logout, name="Logout"),
    url(r'change_contact_details', views.change_contact_details, name="change_contact_details"),
]
