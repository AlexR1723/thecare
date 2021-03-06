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
    url(r'^save_product-image/$', views.Product_image_save, name='Product_image_save'),
    url(r'^dev/$', views.Dev, name="Dev"),
    url(r'^404/$', views.handler404, name="handler404"),
    url(r'^success/$', views.success, name="success"),
    # url(r'^brands/$', views.Brands, name="Brands"),
    # url(r'^news/$', views.News, name="News"),
    # url(r'^news_details/$', views.News_details, name="News_details"),
    # url(r'^search_results/$', views.Search_results, name="Search_results"),

    url(r'^log_in/$', views.Log_in, name="Log_in"),
    url(r'^registration/$', views.Registration, name="Registration"),

    url(r'check_login', views.check_login, name='check_login'),
    url(r'check_register', views.check_register, name='check_register'),

    url(r'top_product_save', views.top_product_save, name='top_product_save'),
    url(r'save_product', views.save_product, name='save_product'),
    url(r'del_product_top', views.del_product_top, name='del_product_top'),
    url(r'check_picture', views.check_picture, name='check_picture'),
    url(r'get_product_count', views.get_product_count, name='get_product_count'),
    url(r'get_product_list', views.get_product_list, name='get_product_list'),
    url(r'get_top', views.get_top, name='get_top'),
    url(r'clear_cache', views.clear_cache, name='clear_cache'),
    # url(r'get_brands_list', views.get_brands_list, name='get_brands_list'),
    # url(r'get_sale_brand', views.get_sale_brand, name='get_sale_brand'),

    # url(r'^$', views.Main, name="Main"),
    # url(r'^dev/$', views.Dev, name="Dev"),
    # url(r'^delivery/$', views.Deliveries, name="Deliveries"),
    # url(r'^payment/$', views.Payments, name="Payments"),
    # url(r'^contacts/$', views.Contacts, name="Contacts"),
    # url(r'^items_catalog/$', views.Items_catalog, name="Items_catalog"),
    # url(r'^face/$', views.Face, name="Face"),
    url(r'^robots.txt$', views.robots_txt, name="robots_txt"),
    url(r'^sitemap.xml', views.sitemap_xml, name="sitemap_xml"),

]

