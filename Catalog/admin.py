from django.contrib import admin
from .models import *
# from django.contrib import admin
# from django.http import HttpResponseRedirect
# from django.conf.urls import url
# from monitor.models import LoginMonitor
# from monitor.import_custom import ImportCustom
# # Register your models here.
#
# @admin.register(LoginMonitor)
# class LoginMonitorAdmin(admin.ModelAdmin):
#     change_list_template = "admin/monitor_change_list.html"
#
#     def get_urls(self):
#         urls = super(LoginMonitorAdmin, self).get_urls()
#         custom_urls = [url('^import/$', self.process_import, name='process_import'),]
#         return custom_urls + urls
#
#
#     def process_import_btmp(self, request):
#         import_custom = ImportCustom()
#         count = import_custom.import_data()
#         self.message_user(request, r"создано {count} новых записей")
#         return HttpResponseRedirect("../")


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



class ProductToneAdmin(admin.TabularInline):
    model = ProductTone


class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    inlines = [ProductNeedAdmin, ProductToneAdmin]
    exclude = ('slug',)

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)