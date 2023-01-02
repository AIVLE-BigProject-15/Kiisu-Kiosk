import cv2
import joblib
import string
import numpy as np

from django.conf import settings
from keras.models import load_model

from glob import iglob
from os.path import join as pjoin

class Classifier:
    def __init__(self, model_name, model_type="CNN", height=128, width=128, channel=1):
        model_path = pjoin(settings.MODEL_DIR, model_name)
        
        if model_type == "CNN":
            self.cls = CNNClassifier(model_path)
        else:
            self.cls = None

        self.height = height
        self.width = width
        self.channel = channel
        
        class_names = list(string.ascii_lowercase)
        self.class_map = {i: class_names[i] for i in range(len(class_names))}
        
    def preprocess(self, img_path):
        flag = cv2.IMREAD_GRAYSCALE if self.channel == 1 else cv2.IMREAD_COLOR
        
        img = cv2.imread(img_path, flag)
        resize_img = cv2.resize(img, (self.height, self.width))
        scaled_img = resize_img / 255.
        
        return scaled_img
    
    def predict(self, img_path):
        img = self.preprocess(img_path=img_path)
        resized_img = img.reshape(-1, self.height, self.width, self.channel)
        pred, prob = self.cls.predict(img=resized_img)
        print(pred, prob)
        return self.class_map[pred], prob


class CNNClassifier():
    def __init__(self, model_path=None):
        self.model = load_model(model_path)

    def predict(self, img):
        pred = self.model.predict(img)
        prob = np.max(pred, axis=1)[0]
        pred = np.argmax(pred, axis=1)[0]
        
        return pred, prob
    
