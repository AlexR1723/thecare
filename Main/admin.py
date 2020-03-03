from django.contrib import admin
from .models import *

class SliderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Slider._meta.fields]

    class Meta:
        model = Slider

admin.site.register(Slider, SliderAdmin)



class MainBlockAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MainBlock._meta.fields]

    class Meta:
        model = MainBlock

admin.site.register(MainBlock, MainBlockAdmin)
