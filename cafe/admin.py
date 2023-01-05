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
        for v in qs.values('id').distinct():
            title = Menu.objects.get(id__exact=v['id']).title            
            context += [{"label" : title, "value" : len(Order.objects.filter(menu__exact=v['id']))}]
        
        context = sorted(context, key=lambda x: x['value'], reverse=True)
        response.context_data['context'] = context
        print(context)
        return response
    
class CustomerAdmin(admin.ModelAdmin):
    list_display=['age_group', 'created']
        
    
class OrderAdmin(admin.ModelAdmin):
    list_display=['id', 'menu', 'created']
    def changelist_view(self, request, extra_context=None):
        response = super(OrderAdmin, self).changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        context = {}
        
        qs = Order.objects.select_related('customer')

        for age in [f'{i}0' for i in range(1, 7)]:
            sub_qs = qs.filter(customer__age_group=f"{age}")
            sub_menu_ids = list(sub_qs.values('menu_id').annotate(total=Count('menu_id')).order_by("count")[:5])
            
            sub_ctx = []
            for x in sub_menu_ids:
                print(x)
                menu = Menu.objects.get(id__exact=x['menu_id']).title
                sub_ctx += [{'label' : menu, 'value': x['total']}]
                
            sub_ctx = sorted(sub_ctx, key=lambda x: x['value'], reverse=True)
            
            context[f'{age}'] = sub_ctx
            
        response.context_data['context'] = context
        print(context)
        return response
    
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