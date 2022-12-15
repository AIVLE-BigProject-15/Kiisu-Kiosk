from django.contrib import admin
from django.conf import settings
from django.db.models import Count
from .models import *

class MenuAdmin(admin.ModelAdmin):
    list_display=['type', 'title', 'price']
    
    def changelist_view(self, request, extra_context=None):
        response = super(MenuAdmin, self).changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        context = []
        # print("queryset", qs)
        for v in qs.values('id').distinct():
            title = Menu.objects.get(id__exact=v['id']).title
            # print(len(Order.objects.filter(menu__exact=v['id'])))            
            # if v.count() > 0:
            
            context += [{"label" : title, "value" : len(Order.objects.filter(menu__exact=v['id']))}]
        
        response.context_data['context'] = context
        print(context)
        return response
    
class CustomerAdmin(admin.ModelAdmin):
    list_display=['age_group', 'version', 'created']
    
class OrderAdmin(admin.ModelAdmin):
    list_display=['id', 'menu', 'created']
    
class ModelAdmin(admin.ModelAdmin):
    list_display=['version', 'pub_date', 'is_active']
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