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
    url(r'^$', views.Main, name="Main"),
    url(r'^save_excel-file/$',views.Save_excel_file, name="Save_excel_file"),
    url(r'^dev/$', views.Dev, name="Dev"),
    # url(r'^brands/$', views.Brands, name="Brands"),
    # url(r'^news/$', views.News, name="News"),
    # url(r'^news_details/$', views.News_details, name="News_details"),
    # url(r'^search_results/$', views.Search_results, name="Search_results"),

    url(r'^log_in/$', views.Log_in, name="Log_in"),
    url(r'^registration/$', views.Registration, name="Registration"),
    url(r'^orders_history/$', views.Orders_history, name="Orders_history"),
    url(r'^delivery_address/$', views.Delivery_address, name="Delivery_address"),
    url(r'check_login', views.check_login, name='check_login'),
    url(r'check_register', views.check_register, name='check_register'),

    # url(r'^$', views.Main, name="Main"),
    # url(r'^dev/$', views.Dev, name="Dev"),
    # url(r'^delivery/$', views.Deliveries, name="Deliveries"),
    # url(r'^payment/$', views.Payments, name="Payments"),
    # url(r'^contacts/$', views.Contacts, name="Contacts"),
    # url(r'^items_catalog/$', views.Items_catalog, name="Items_catalog"),
    # url(r'^face/$', views.Face, name="Face"),
]
