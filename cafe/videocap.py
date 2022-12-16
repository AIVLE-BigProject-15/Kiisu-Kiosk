import cv2
import threading

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        gray_img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        return gray_img

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


class CameraInstance:
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance

class MyCamera(VideoCamera, CameraInstance):
    pass
