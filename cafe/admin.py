from django.contrib import admin
from django.conf import settings
from .models import *

class MenuAdmin(admin.ModelAdmin):
    list_display=['type', 'title', 'price']
    
class CustomerAdmin(admin.ModelAdmin):
    list_display=['age_group', 'version', 'created']
    
class OrderAdmin(admin.ModelAdmin):
    list_display=['id', 'menu', 'created']
    
class ModelAdmin(admin.ModelAdmin):
    list_display=['version', 'type', 'is_active']
    actions=['activate', 'deactivate']

    def activate(self, request, queryset):
        queryset.update(is_active= True ) #queryset.update
    activate.short_description = '지정 모델을 active 상태로 변경'
    
    def deactivate(self, request, queryset):
        queryset.update(is_active= False) #queryset.update
    deactivate.short_description = '지정 모델을 deactive 상태로 변경'
        
admin.site.register(Menu, MenuAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Model, ModelAdmin)