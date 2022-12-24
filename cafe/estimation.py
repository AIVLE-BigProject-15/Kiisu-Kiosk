import cv2
import threading

class Estimations(object):
    def __init__(self):
        self.history = []

    def add(self, pred):
        self.history += [pred]
        
    def get_last(self):
        if self.history:
            return self.history[-1]
        return -1

class EstimationsInstance:
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance

class MyEstimations(Estimations, EstimationsInstance):
    pass

