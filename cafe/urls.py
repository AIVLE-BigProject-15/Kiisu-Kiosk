
from django.urls import path, include

from . import views
app_name = 'cafe'
urlpatterns = [
    path('', views.home, name='home'),
    path('young_order', views.young_order, name='young_order'),
    path('old_order', views.old_order, name='old_order'),
    path('old_confirm', views.old_confirm, name='old_confirm'),
    path('old_pay', views.old_pay, name='old_pay'),
    path('img_post', views.get_post),
    path('camera', views.camera, name='camera'),
    path('check', views.check, name='check'),

]


