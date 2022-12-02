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
    menu_list = Menu.objects.all()
    return render(request, 'cafe/order.html', {'menu_all':menu_list})


def temp(request):
    hot_cf_list = Menu.objects.filter(type__icontains="hot")
    ice_cf_list = Menu.objects.filter(type__icontains="ice")
    non_cf_list = Menu.objects.filter(type__icontains="non")
    smoothie_list = Menu.objects.filter(type__icontains="smoothie")
    bread_list = Menu.objects.filter(type__icontains="bread")

    return render(request, 'cafe/temp.html', {'hot_coffee_all':hot_cf_list,
                                              'ice_coffee_all' : ice_cf_list,
                                              'non_coffee_all' : non_cf_list,
                                              'smoothie_all' : smoothie_list,
                                              'bread_all' : bread_list,
                                              })
