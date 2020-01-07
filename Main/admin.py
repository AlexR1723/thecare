from django.contrib import admin
from .models import *

# Register your models here.

class CategoryTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CategoryType._meta.fields]

    class Meta:
        model = CategoryType

admin.site.register(CategoryType, CategoryTypeAdmin)


class NeedTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in NeedType._meta.fields]

    class Meta:
        model = NeedType

admin.site.register(NeedType, NeedTypeAdmin)


class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ResourceType._meta.fields]

    class Meta:
        model = ResourceType

admin.site.register(ResourceType, ResourceTypeAdmin)


class ProductNeedAdmin(admin.TabularInline):
    model = ProductNeed


class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    inlines = [ProductNeedAdmin]

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)