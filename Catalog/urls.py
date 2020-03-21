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
    # url(r'^for_men/$', views.For_men, name="For_men"),
    # url(r'^for_men/(?P<filter>[a-z_]+)/$', views.For_men_filter, name="For_men_filter"),
    # url(r'^for_men/(?P<page>[0-9]+)/$', views.For_men_page, name="For_men_page"),
    # url(r'^for_men/(?P<page>[0-9]+)/(?P<filter>[a-z_]+)/$', views.For_men_page_filter, name="For_men_page_filter"),
    # url(r'^for_men/(?P<text>[^/]+)/$', views.For_men_search, name="For_men_search"),
    # url(r'^for_men/(?P<text>[^/]+)/(?P<filter>[a-z_]+)/$', views.For_men_search_filter, name="For_men_search_filter"),
    # url(r'^for_men/(?P<text>[^/]+)/(?P<page>[^/]+)/$', views.For_men_search_page, name="For_men_search_page"),
    # url(r'^for_men/(?P<text>[^/]+)/(?P<page>[^/]+)/(?P<filter>[a-z_]+)/$', views.For_men_search_page_filter,
    #     name="For_men_search_page_filter"),

    url(r'^(?P<head_url>[A-Za-zА-Яа-я_]+)/$', views.Catalog, name="Catalog"),
    url(r'^(?P<head_url>[A-Za-zА-Яа-я_]+)/(?P<filter>[a-z_]+)/$', views.Catalog_filter, name="Catalog_filter"),
    url(r'^(?P<head_url>[A-Za-zА-Яа-я_]+)/(?P<page>[0-9]+)/$', views.Catalog_page, name="Catalog_page"),
    url(r'^(?P<head_url>[A-Za-zА-Яа-я_]+)/(?P<page>[0-9]+)/(?P<filter>[a-z_]+)/$', views.Catalog_page_filter, name="Catalog_page_filter"),
    url(r'^(?P<head_url>[A-Za-zА-Яа-я_]+)/(?P<text>[^/]+)/$', views.Catalog_search, name="Catalog_search"),
    url(r'^(?P<head_url>[A-Za-zА-Яа-я_]+)/(?P<text>[^/]+)/(?P<filter>[a-z_]+)/$', views.Catalog_search_filter, name="Catalog_search_filter"),
    url(r'^(?P<head_url>[A-Za-zА-Яа-я_]+)/(?P<text>[^/]+)/(?P<page>[^/]+)/$', views.Catalog_search_page, name="Catalog_search_page"),
    url(r'^(?P<head_url>[A-Za-zА-Яа-я_]+)/(?P<text>[^/]+)/(?P<page>[^/]+)/(?P<filter>[a-z_]+)/$', views.Catalog_search_page_filter,
        name="Catalog_search_page_filter"),

    url(r'^items_catalog/$', views.Items_catalog, name="Items_catalog"),
    url(r'get_product_sizes', views.get_product_sizes, name="get_product_sizes"),
    # url(r'^search_results/$', views.Search_results, name="Search_results"),
    # url(r'^item_card/$', views.Item_card, name="Item_card"),
    path('<slug:slug>', views.Item_card, name='Item_card'),
]
