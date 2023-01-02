#pragma warning (disable:-1072873821)

import os, json, time
from .models import *
from os.path import join as pjoin
import cv2
import joblib

import warnings
warnings.filterwarnings(action='ignore')

from django.conf import settings
from django.db.models import Count

from django.utils import timezone
from django.http import JsonResponse
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from .videocap import MyCamera
from PIL import Image
from keras.models import load_model
import numpy as np


MODEL_NAME = "face_10s4.h5" # 모델명 쓰는 곳
MODEL_TYPE = "CNN"

def home(request):
    return render(request, 'cafe/home.html')


def old_order(request):
    age = request.GET.get('age')
    
    qs = Order.objects.select_related('customer')
    sub_qs = qs.filter(customer__age_group=f"{age}")
    sub_menu_ids = list(sub_qs.values('menu_id').annotate(total=Count('menu_id')).order_by("count")[:5])
    sub_menu_ids = list(map(lambda x: x['menu_id'], sub_menu_ids))
    
    best_menu_all= Menu.objects.filter(id__in=sub_menu_ids)
    
    hot_cf_list = Menu.objects.filter(type__in=['hot_coffee', 'ice_coffee'])    
    non_cf_list = Menu.objects.filter(type__in=['non_coffee', 'smoothie'])
    
    bread_list = Menu.objects.filter(type__icontains="bread")

    page_url = "cafe/old_order.html"
    
    return render(request, page_url, {'hot_coffee_all':hot_cf_list,
                                              'non_coffee_all' : non_cf_list,
                                              'bread_all' : bread_list,
                                              'best_menu_all' : best_menu_all,
                                              })


def check(request, context):
    return render(request, "cafe/check.html", context)
    
    
def young_order(request):    
    context = {}
    if request.method == "POST":
        usage_type = request.POST.get('usage_type')
        menu_list = request.POST.getlist('menu_list')[0].split(",")
        menu_counts = list(map(int, request.POST.getlist('menu_counts')[0].split(",")))
        customer_obj = Customer.objects.filter(id__exact=request.POST.get('customer_id'))[0]

        print(menu_list)
        print(menu_counts)
        for menu_title, cnt in zip(menu_list, menu_counts):
            menu_obj = Menu.objects.filter(title__exact=menu_title)[0]
            
            order_obj = Order()
            order_obj.menu = menu_obj
            order_obj.customer = customer_obj
            order_obj.count = cnt

            order_obj.created = timezone.datetime.now()
            order_obj.save()
                
        context['usage_type'] = usage_type
        context['order_id'] = order_obj.id
        return check(request, context)
    
    age = request.GET.get('age')
    print(age)
    
    qs = Order.objects.select_related('customer')
    sub_qs = qs.filter(customer__age_group=f"{age}")
    sub_menu_ids = list(sub_qs.values('menu_id').annotate(total=Count('menu_id')).order_by("count")[:5])
    sub_menu_ids = list(map(lambda x: x['menu_id'], sub_menu_ids))
    best_menu_all= Menu.objects.filter(id__in=sub_menu_ids)
    print(best_menu_all)
                            
    context = {'hot_coffee_all': Menu.objects.filter(type__icontains="hot"),
                'ice_coffee_all' : Menu.objects.filter(type__icontains="ice"),
                'non_coffee_all' : Menu.objects.filter(type__icontains="non"),
                'smoothie_all' : Menu.objects.filter(type__icontains="smoothie"),
                'bread_all' : Menu.objects.filter(type__icontains="bread"),
                'cookie_all' : Menu.objects.filter(type__icontains="cookie"),
                'best_menu_all' : best_menu_all,
            }
    return render(request, "cafe/young_order.html", context)
    
def old_confirm(request):
    context = {}
    if request.method == "POST":
        usage_type = request.POST.get('usage_type')
        menu_list = request.POST.getlist('menu_list')[0].split(",")
        menu_counts = list(map(int, request.POST.getlist('menu_counts')[0].split(",")))

        print(menu_list)
        print(menu_counts)
        
        order_list = []
        total_price = 0
        for menu_title, cnt in zip(menu_list, menu_counts):
            menu_obj = Menu.objects.filter(title__exact=menu_title)[0]
            total_price += menu_obj.price * int(cnt)
            order_list += [{'menu' : menu_obj, 'cnt' : cnt}]
        
        context['usage_type'] = usage_type
        context['total_count'] = sum(menu_counts)
        context['order_list'] = order_list
        context['customer_id'] = request.POST.get('customer_id')
        context['total_price'] = total_price
                
        print(context)
    else:
        pass
        
    return render(request, 'cafe/old_confirm.html', context)   

def old_pay(request):
    context = {}
    if request.method == "POST":
        usage_type = request.POST.get('usage_type')
        menu_list = request.POST.getlist('menu_list')[0].split(",")
        menu_counts = list(map(int, request.POST.getlist('menu_counts')[0].split(",")))
        customer_obj = Customer.objects.filter(id__exact=request.POST.get('customer_id'))[0]

        print(menu_list)
        print(menu_counts)
        order_list = []
        for menu_title, cnt in zip(menu_list, menu_counts):
            menu_obj = Menu.objects.filter(title__exact=menu_title)[0]
            
            order_obj = Order()
            order_obj.menu = menu_obj
            order_obj.customer = customer_obj
            order_obj.count = cnt

            order_obj.created = timezone.datetime.now()
            order_obj.save()
            
            order_list += [order_obj.id]
        
        context['usage_type'] = usage_type
        context['order_id'] = order_list[-1]
                
        return render(request, "cafe/check.html", context)         

def get_face(image):
    file_path = settings.MODEL_DIR + '/haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(file_path)

    
    faces = faceCascade.detectMultiScale(
        image, #grayscale로 이미지 변환한 원본.
        scaleFactor=1.2, #이미지 피라미드에 사용하는 scalefactor
        minNeighbors=3, #최소 가질 수 있는 이웃으로 3~6사이의 값을 넣어야 detect가 더 잘된다고 한다
        minSize=(20, 20)
    )

    print(faces)
    if not faces == ():
        x, y, w, h = faces[0]
        cur_img = image[y:y+h, x:x + w]
        cv2.rectangle(faces,(x,y),(x+w,y+h),(255,255,255),2)
        cv2.imwrite('temp.jpg', cur_img)
        return cur_img
        
    return


# 모델의 경로를 불러온다.
def predicting_model():
    model_obj = Model.objects.filter(is_active = True)[0]
    print(model_obj.model.path)
    return joblib.load(model_obj.model.path)

def classify(face_img):
    print(face_img.shape)
    features = []
    character = {0:'10대', 1:'20대', 2:'30대', 3:'40대', 4:'50대', 5:'60대 이상'}
        
    img = cv2.resize(face_img, (128, 128), Image.ANTIALIAS)
    
    
    img = np.array(img)
    features.append(img)
    features = np.array(features)
    
    # ignore this step if using RGB
    features = features.reshape(-1, 128, 128, 1) # len(features)
    features = features / 255.0

    # 불러온 모델의 경로로 예측
    model_path = settings.MODEL_DIR + f"/{MODEL_NAME}"
    print(model_path)
    model = load_model(model_path)
    
    pred = model.predict(features[0].reshape(-1, 128, 128, 1))
    
    pred_array = np.zeros(shape=(pred.shape[0], pred.shape[1]))
    pred_array[0][pred.argmax()] = 1

    # 여기는 나이대랑 사진 보이는 코드
    print({character[pred_array[0].argmax()]})

    return character[pred_array[0].argmax()]


from PIL import Image, ImageDraw

def camera(request):
    if request.method == "POST":
        age_group = request.POST.get("age_group")
        print(age_group)
        
        # Customer 생성
        customer_obj = Customer()
        customer_obj.age_group = age_group
        customer_obj.created = timezone.datetime.now()
        customer_obj.save()
        
        print("Customer 생성")
        
        return HttpResponse(customer_obj.id)

    return render(request, 'cafe/camera.html')
    

# 앱에서 받은 img predict, --csrf 예외처리--
@csrf_exempt
def get_post(request):
    data={}
    if request.method =='POST':
        image_ = request.FILES['image']
        data = {'image':image_}
        
        img = Image.open(data['image'].file)
        gray_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
        
        face_img = get_face(gray_img)
        age_group = classify(face_img)
        print(age_group)
        return HttpResponse(age_group)
    return render(request, 'cafe\parameter.html', data)
        

