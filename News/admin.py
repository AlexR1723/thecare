from django.contrib import admin
from .models import *


class NewsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in News_model._meta.fields]
    # list_filter = ['type']
    exclude = ('slug','date')

    class Meta:
        model = News_model


admin.site.register(News_model, NewsAdmin)
