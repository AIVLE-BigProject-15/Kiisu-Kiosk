import os, json
from .models import *
from os.path import join as pjoin

from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect


def home(request):
    return render(request, 'cafe/home.html')

def chunks(lst, n):
    i = 0
    while i < len(lst):
        yield lst[i:i + n]
        i += n
        

def order(request):
    hot_cf_list = Menu.objects.filter(type__icontains="hot")
    ice_cf_list = Menu.objects.filter(type__icontains="ice")
    non_cf_list = Menu.objects.filter(type__icontains="non")
    smoothie_list = Menu.objects.filter(type__icontains="smoothie")
    bread_list = Menu.objects.filter(type__icontains="bread")

    return render(request, 'cafe/order.html', {'hot_coffee_all':hot_cf_list,
                                              'ice_coffee_all' : ice_cf_list,
                                              'non_coffee_all' : non_cf_list,
                                              'smoothie_all' : smoothie_list,
                                              'bread_all' : bread_list,
                                              })
    
def confirm(request):
    context = {}
    if request.method == "POST":

        usage_type = request.POST.get('usage_type')
        menu_list = request.POST.getlist('menu_list')[0].split(",")
        menu_counts = list(map(int, request.POST.getlist('menu_counts')[0].split(",")))
        # customer_obj = Customer.objects.filter(id__exact=request.POST.get('customer_id'))[0]

        print(menu_list)
        print(menu_counts)
        cart_list = []
        total_price = 0
        for menu_title, cnt in zip(menu_list, menu_counts):
            menu_obj = Menu.objects.filter(title__exact=menu_title)[0]
            
            order_obj = Order()
            order_obj.menu = menu_obj
            order_obj.count = cnt

            order_obj.created = timezone.datetime.now()
            order_obj.save()
        
            cart_list += [order_obj]
            total_price += menu_obj.price * int(cnt)
        
        context['usage_type'] = usage_type
        context['total_count'] = sum(list(map(lambda x: x.count, cart_list)))
        context['cart_all'] = cart_list
        context['total_price'] = total_price
        
        print(context)
    else:
        pass
        
    return render(request, 'cafe/confirm.html', context)        

def pay(request):
    context = {}
    if request.method == "POST":
        usage_type = request.POST.get('usage_type')
        total_price = request.POST.get('total_price')
        order_ids = list(map(int, request.POST.getlist('orders')[0].split(",")))
        # customer_obj = Customer.objects.filter(id__exact=request.POST.get('customer_id'))[0]

        print(usage_type)
        print(total_price)
        print(order_ids)
        
        context['usage_type'] = usage_type
        context['order_ids'] = order_ids
        context['total_price'] = total_price
        
        print(context)
    else:
        pass
        
    return render(request, 'cafe/pay.html', context)        