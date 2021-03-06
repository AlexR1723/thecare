"""the_care URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', include('Main.urls')),
    url(r'delivery/', include('Delivery.urls')),
    url(r'news/', include('News.urls')),
    url(r'payment/', include('Payment.urls')),
    url(r'contacts/', include('Contacts.urls')),
    url(r'catalog/', include('Catalog.urls')),
    url(r'brands/', include('Brands.urls')),
    url(r'cart/', include('Basket.urls')),
    url(r'profile/', include('Profile.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'Main.views.handler404'
