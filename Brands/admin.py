from django.contrib import admin
from .models import *

# Register your models here.
class Brands_modelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Brands_model._meta.fields]

    class Meta:
        model = Brands_model

admin.site.register(Brands_model, Brands_modelAdmin)
