import os, json
from .models import *
from os.path import join as pjoin

from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect


def home(request):
    return render(request, 'cafe/home.html')

def order(request):
    menu_list = Menu.objects.all()
    print(menu_list)
    print(menu_list.get(id=1).image)
    return render(request, 'cafe/order.html', {'menu_all':menu_list})
