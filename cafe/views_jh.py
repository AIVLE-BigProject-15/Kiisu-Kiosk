import os, json
from .models import *
from os.path import join as pjoin
import cv2
import joblib

from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect

from .videocap import MyCamera
from .classify import Classifier
from PIL import Image
from keras.models import load_model
import numpy as np


MODEL_NAME = "agebase.h5" # 모델명 쓰는 곳
MODEL_TYPE = "CNN"

classifier = Classifier(model_name=MODEL_NAME, model_type=MODEL_TYPE)

def home(request):
    return render(request, 'cafe/home.html')

def chunks(lst, n):
    i = 0
    while i < len(lst):
        yield lst[i:i + n]
        i += n


def order(request, age_group="(60, 100)"):
    hot_cf_list = Menu.objects.filter(type__icontains="hot")
    ice_cf_list = Menu.objects.filter(type__icontains="ice")
    non_cf_list = Menu.objects.filter(type__icontains="non")
    smoothie_list = Menu.objects.filter(type__icontains="smoothie")
    bread_list = Menu.objects.filter(type__icontains="bread")

    page_url = "cafe/order.html" if int(age_group[1]) < 6 else "cafe/old_order.html"

    return render(request, page_url, {'hot_coffee_all':hot_cf_list,
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

def get_face():
    file_path = settings.MODEL_DIR + '/haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(file_path)

    # 비디오의 setting을 준비함.
    cap = MyCamera.instance()
    print("Start")
    
    while True:
        frame = cap.get_frame_jh()
        faces = faceCascade.detectMultiScale(
            frame, #grayscale로 이미지 변환한 원본.
            scaleFactor=1.2, #이미지 피라미드에 사용하는 scalefactor
            minNeighbors=3, #최소 가질 수 있는 이웃으로 3~6사이의 값을 넣어야 detect가 더 잘된다고 한다
            minSize=(20, 20)
        )

        if not faces == ():
            x, y, w, h = faces[0]
            cur_img = frame[y:y+h, x:x + w]
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),2)
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
    character = {0:'(0, 3)', 1:'(15, 24)', 2:'(25, 37)', 3:'(38, 47)', 4:'(4, 7)', 5:'(48, 59)',6:'(60, 100)',7:'(8, 14)'}

    # 넘파이 형태 -> 이미지 형태로 전환
    # img = Image.fromarray(face_img)
    #######################################
    
    # img = img.astype(np.uint8).copy()
    # img = cv2.imread(face_img, cv2.IMREAD_GRAYSCALE)
    
    img = cv2.resize(face_img, (128, 128), Image.ANTIALIAS)
    
    
    img = np.array(img)
    features.append(img)
    features = np.array(features)
    
    # ignore this step if using RGB
    features = features.reshape(-1, 128, 128, 3)
    features = features / 255.0
    
    # 불러온 모델의 경로로 예측
    model_path = settings.MODEL_DIR + '/agebase.h5'
    # model_path = predicting_model()
    model = load_model(model_path)
    
    pred = model.predict(features[0].reshape(-1, 128, 128, 3))
    
    pred_array = np.zeros(shape=(pred.shape[0], pred.shape[1]))
    pred_array[0][pred.argmax()] = 1

    # 여기는 나이대랑 사진 보이는 코드
    print({character[pred_array[0].argmax()]})
    #plt.axis('off')
    #plt.imshow(features[0].reshape(128, 128), cmap='gray') 
    
    # model_path = pjoin(settings.MODEL_DIR, model_name)
    # model_path = settings.MODEL_DIR + '/face_10s2.h5'
    # model = load_model(model_path)
    
    # result = model.predict(face_img)
    
    return character[pred_array[0].argmax()]

def detect_age_group(request):
    face = get_face()
    age_group = classify(face) 

    return order(request, age_group=age_group)    

from PIL import Image, ImageDraw

def camera(request):
    if request.method == "POST" and request.FILES:
        usage_type = request.POST.get("usage_type")
        box = json.loads(request.POST.get("box"))
        face_image = request.FILES['face_image']
        
        img = Image.open(face_image.file)
        x, y, w, h = map(lambda x: int(box[x]), box)

        draw = ImageDraw.Draw(img)
        draw.rectangle((x, y, x + w, y + h), outline=(255, 0, 0), width = 3)
        crop_img = img.crop((x, y, x + w, y + h))
        
        img.save('test_img.png',"PNG")
        crop_img.save('test_crop_img.png',"PNG")
        
        gray_img = cv2.cvtColor(np.array(crop_img) , cv2.COLOR_RGB2GRAY)
        age_group = classify(gray_img)
        print(age_group, usage_type)
        
        page_url = "order" if int(age_group[0]) < 4 else "old_order"
        return HttpResponse(page_url + f"?usage_type={usage_type}")

    return render(request, 'cafe/camera.html')

from .serializer import CustomerSerializer
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

class fetch_user(ListAPIView):
        
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

