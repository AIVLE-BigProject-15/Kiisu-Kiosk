import os, json
from .models import *
from os.path import join as pjoin
import cv2

from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect

from .classify import Classifier
from PIL import Image
from keras.models import load_model
import numpy as np


MODEL_NAME = "face_10s2.h5" # 모델명 쓰는 곳
MODEL_TYPE = "CNN"

classifier = Classifier(model_name=MODEL_NAME, model_type=MODEL_TYPE)

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
 
def get_face():
    file_path = settings.MODEL_DIR + '/haarcascade_frontalface_default.xml'
    
    faceCascade = cv2.CascadeClassifier(file_path)

    # 비디오의 setting을 준비함.
    cap = cv2.VideoCapture(0) #0번이 내장카메라, 1번이 외장카메라
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("Start")
    while True:
        ret, img = cap.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale( 
            gray, #grayscale로 이미지 변환한 원본.
            scaleFactor=1.2, #이미지 피라미드에 사용하는 scalefactor
            minNeighbors=3, #최소 가질 수 있는 이웃으로 3~6사이의 값을 넣어야 detect가 더 잘된다고 한다.

            minSize=(20, 20) 
        )

        if not faces == ():
            x, y, w, h = faces[0]
            cur_img = img[x:x + w, y:y+h]
            return cur_img
        
        #영상에 img 값을 출력
        cv2.imshow('video',img)
        # video라는 이름으로 출력
        k = cv2.waitKey(1) & 0xff #time값이 0이면 무한 대기, waitKey는 키가 입력 받아 질때까지 기다리는 시간을 의미한다.
        #FF는 끝의 8bit만을 이용한다는 뜻으로 ASCII 코드의 0~255값만 이용하겠다는 의미로 해석됨. (NumLock을 켰을때 또한 )
        if k == 27: # press 'ESC' to quit # ESC를 누르면 종료
            break
        
        cap.release() #비디오 끄기   (카메라 리소스 헤제)
        cv2.destroyAllWindows()
        return

def classify(face_img):
    
    features = []
    character = {0:'10대', 1:'20대', 2:'30대', 3:'40대', 4:'50대', 5:'60대 이상'}
    
    img = cv2.imread(face_img, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (128, 128), Image.ANTIALIAS)
    
    img = np.array(img)
    features.append(img)
    features = np.array(features)
    
    # ignore this step if using RGB
    features = features.reshape(len(features), 128, 128, 1)
    features = features / 255.0
    
    model_path = settings.MODEL_DIR + '/face_10s2.h5'
    model = load_model(model_path)
    
    pred = model.predict(features[0].reshape(1, 128, 128, 1))
    pred_array = np.zeros(shape=(pred.shape[0], pred.shape[1]))
    pred_array[0][pred.argmax()] = 1

    # 여기는 나이대랑 사진 보이는 코드
    print({character[pred_array[0].argmax()]})
    #plt.axis('off')
    #plt.imshow(features[0].reshape(128, 128), cmap='gray') 
    
    
    #model_path = pjoin(settings.MODEL_DIR, model_name)

    # model_path = settings.MODEL_DIR + '/face_10s2.h5'
    # model = load_model(model_path)
    
    # result = model.predict(face_img)
    
    return pred

def detect_age_group(request):
    face = get_face()
    age_group = classify(face)
    
    if age_group == 'senior':
        return render(request, 'cafe/old_order.html')
    else:
        return render(request, 'cafe/order.html')
