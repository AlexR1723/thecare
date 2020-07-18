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
    url(r'^$', views.Cart, name="Cart"),
    url(r'add_product', views.add_product, name="add_product"),
    url(r'plus_minus_product', views.plus_minus_product, name="plus_minus_product"),
    url(r'del_product', views.del_product, name="del_product"),
    url(r'buy_products', views.buy_products, name="buy_products"),
    url(r'confirm_order', views.confirm_order, name="confirm_order"),
    url(r'pay_result', views.pay_result, name="pay_result"),
    url(r'pay_success', views.pay_success, name="pay_success"),
    url(r'pay_fail', views.pay_fail, name="pay_fail"),
    url(r'pay_check', views.pay_check, name="pay_check"),

]
